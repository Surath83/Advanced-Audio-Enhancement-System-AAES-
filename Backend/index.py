import os
import sys
import json
import time
import numpy as np
import soundfile as sf
from report import generate_report
from report import append_report_to_excel
from scipy.signal import butter, filtfilt, lfilter
from pydub import AudioSegment
from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
import librosa

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

STANDARD_FREQS = np.array([125, 250, 500, 1000, 2000, 4000, 8000])


# ----------------------------------------
# AUDIO UTILITIES (with logs)
# ----------------------------------------

# Convert Any Audio to WAV
def convert_to_wav(input_path):
    print(f"🔍 Converting to WAV (if necessary): {input_path}")
    output_path = input_path.rsplit(".", 1)[0] + ".wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(2)
    audio.export(output_path, format="wav")
    return output_path

# Load Stereo Audio File
def load_audio(audio_path):
    print(f"🎵 Loading audio: {audio_path}")
    try:
        y, sr = librosa.load(audio_path, sr=None, mono=False)
        if y.ndim == 1:
            y = np.vstack((y, y))
        return y[0], y[1], sr
    except Exception as e:
        raise ValueError(f"❌ Error loading audio: {e}")

# Ensure Both Channels Have the Same Length
def match_audio_lengths(left, right):
    max_length = max(len(left), len(right))
    left = np.pad(left, (0, max_length - len(left)), mode='constant')
    right = np.pad(right, (0, max_length - len(right)), mode='constant')
    return left, right


# ----------------------------------------
# NOISE REDUCTION / FILTERS / EFFECTS
# ----------------------------------------

# MMSE Noise Reduction (operates on stereo/multi -> returns stereo)
def mmse_filter(audio, sr, noise_estimation_duration=1.0):
    print("🔇 Reducing noise using MMSE")

    # audio shape: (2, N) or (N,) -> convert to mono for noise estimation
    if audio.ndim == 2:
        audio_mono = np.mean(audio, axis=0)
    else:
        audio_mono = audio

    noise_samples = int(noise_estimation_duration * sr)
    if noise_samples < 1:
        noise_samples = 1
    noise_estimate = audio_mono[:noise_samples]

    stft_audio = librosa.stft(audio_mono)
    stft_noise = librosa.stft(noise_estimate)

    noise_psd = np.mean(np.abs(stft_noise) ** 2, axis=1)
    audio_psd = np.abs(stft_audio) ** 2

    mmse_gain = audio_psd / (audio_psd + noise_psd[:, np.newaxis] + 1e-8)
    filtered_stft = mmse_gain * stft_audio

    denoised_audio_mono = librosa.istft(filtered_stft, length=len(audio_mono))

    # return stereo by duplicating mono if input was mono, else keep channels similar
    denoised_audio = np.vstack((denoised_audio_mono, denoised_audio_mono))
    return denoised_audio

# STFT-based simple denoising per-channel
def stft_denoising(audio, sr):
    print("✨ Applying STFT Denoising")
    D = librosa.stft(audio)
    magnitude, phase = np.abs(D), np.angle(D)

    threshold = np.median(magnitude)
    magnitude = np.where(magnitude > threshold, magnitude, 0)

    cleaned = magnitude * np.exp(1j * phase)
    return librosa.istft(cleaned, length=len(audio))

# Boost High-Pitch Vocals (highpass + mix)
def high_pitch_boost(audio, sr, boost_db=5, freq=3000):
    print("🎤 Boosting High-Pitch Vocals")
    nyquist = sr / 2.0
    wp = float(freq) / nyquist
    if wp <= 0 or wp >= 1:
        return audio
    b, a = butter(2, wp, btype="high")
    try:
        boosted = filtfilt(b, a, audio)
    except Exception:
        boosted = audio  # fallback if filtfilt fails
    return audio + (boosted * (10 ** (boost_db / 20.0)))

# LMS Adaptive Filter (simple implementation)
def apply_lms_filter(audio, desired=None, mu=0.001, filter_order=32):
    print("🔄 Applying LMS Filter")
    n_samples = len(audio)
    if desired is None:
        desired = audio

    if n_samples <= filter_order:
        return np.copy(audio)

    w = np.zeros(filter_order)
    filtered_audio = np.zeros(n_samples)

    for n in range(filter_order, n_samples):
        x = audio[n - filter_order:n][::-1]
        y = np.dot(w, x)
        e = desired[n] - y
        w += 2 * mu * e * x
        filtered_audio[n] = y

    return filtered_audio

# Vocal Boost (simple gain)
def vocal_boost(left, right):
    print("🎙️ Enhancing Vocals")
    left = left * 1.05
    right = right * 1.05
    return left, right

# Capacitor Effect Simulation (smoothing filter)
def capacitor_effect(audio, sr, smoothing_factor=0.3):
    print("🔋 Applying Capacitor Effect")
    alpha = smoothing_factor
    # simple IIR smoothing: y[n] = alpha * x[n] + (1-alpha)*y[n-1]
    b = [alpha]
    a = [1, alpha - 1]
    return lfilter(b, a, audio)

# Final Volume Boost
def final_volume_boost(audio):
    print("🔊 Increasing Final Volume")
    return audio * 1.1


# ----------------------------------------
# FREQUENCY GAIN (Audiogram) UTILITIES
# ----------------------------------------

def _freqs_for_stft(sr, n_fft):
    return np.linspace(0, sr/2, 1 + n_fft // 2)

def make_gain_curve(sr, n_fft, profile_freqs, profile_db, gain_factor):
    freqs = _freqs_for_stft(sr, n_fft)
    gain_db = np.zeros_like(freqs)
    sigma = 1000.0  # smoothing width in Hz

    for f_center, db in zip(profile_freqs, profile_db):
        applied = db * gain_factor
        gauss = np.exp(-0.5 * ((freqs - f_center) / sigma) ** 2)
        gain_db += applied * gauss

    # convert dB curve to linear amplitude multipliers
    return 10.0 ** (gain_db / 20.0)

def apply_profile_channel(x, sr, prof, gain_factor):
    freqs = STANDARD_FREQS
    dbs = [prof.get(str(int(f)), 0) for f in freqs]

    D = librosa.stft(x, n_fft=2048)
    mag, phase = np.abs(D), np.angle(D)

    gain = make_gain_curve(sr, 2048, freqs, dbs, gain_factor)
    mag2 = mag * gain[:, None]

    out = librosa.istft(mag2 * np.exp(1j * phase), length=len(x))
    return out

def apply_audiogram(L, R, sr, profile, tuning_gain_percent):
    print("🎚 Applying audiogram tuning...")
    gain_factor = float(tuning_gain_percent) / 100.0
    L2 = apply_profile_channel(L, sr, profile["left"], gain_factor)
    R2 = apply_profile_channel(R, sr, profile["right"], gain_factor)
    return match_audio_lengths(L2, R2)


# ----------------------------------------
# MAIN PROCESSOR (merged chain)
# ----------------------------------------

def process_audio_with_full_chain(input_path, output_path, hearing_loss, tuning_gain):
    """
    Full AAES DSP pipeline + reporting hooks.
    """
    try:
        start_time = time.time()

        print(f"🎧 Processing audio (full chain): {input_path}")

        # 1. Convert to WAV if needed
        if not input_path.lower().endswith(".wav"):
            input_path = convert_to_wav(input_path)

        # 2. Load audio
        left, right, sr = load_audio(input_path)

        # FIX: Save ORIGINAL stereo audio for SNR/PESQ/STOI
        original_stereo = np.vstack((left, right))   

        # 3. Combine channels for INITIAL noise reduction
        print("🔰 Initial Noise Reduction (MMSE at beginning)")
        stereo_raw = np.vstack((left, right))
        mmse_initial = mmse_filter(stereo_raw, sr)

        # Extract denoised channels
        left_clean, right_clean = mmse_initial[0], mmse_initial[1]

        # 4. LMS filter
        left_lms = apply_lms_filter(left_clean)
        right_lms = apply_lms_filter(right_clean)

        # 5. STFT denoising (light)
        left_den = stft_denoising(left_lms, sr)
        right_den = stft_denoising(right_lms, sr)

        # 6. High pitch boost
        left_hp = high_pitch_boost(left_den, sr)
        right_hp = high_pitch_boost(right_den, sr)

        # 7. Vocal boost
        left_vb, right_vb = vocal_boost(left_hp, right_hp)

        # 8. Capacitor effect
        left_cap = capacitor_effect(left_vb, sr)
        right_cap = capacitor_effect(right_vb, sr)

        # 9. Match Lengths
        left_m, right_m = match_audio_lengths(left_cap, right_cap)

        # 10. Apply Audiogram Tuning
        left_tuned, right_tuned = apply_audiogram(
            left_m, right_m, sr, hearing_loss, tuning_gain
        )

        # 11. Final Volume Boost
        final_audio = np.vstack((left_tuned, right_tuned))
        final_audio = final_volume_boost(final_audio)

        # 12. SAVE OUTPUT
        sf.write(output_path, final_audio.T, sr)

        end_time = time.time()             
        latency_ms = (end_time - start_time) * 1000.0 

        # ---- GENERATE METRIC REPORT ----
        report_data = generate_report(
            original_audio=original_stereo,
            enhanced_audio=final_audio,
            sr=sr,
            hearing_loss=hearing_loss,
            tuning_gain=tuning_gain,
            latency_ms=latency_ms,
        )
        report_json_path = output_path.replace(".wav", "_report.json")
        with open(report_json_path, "w") as f:
            json.dump(report_data, f, indent=4)

        append_report_to_excel(report_data)
        
        print(f"📄 Report generated at: {report_json_path}")
        print(f"✅ Processing complete: {output_path}")

    except Exception as e:
        print(f"❌ Processing error: {e}")
        raise


# ----------------------------------------
# API ROUTES
# ----------------------------------------

@app.route("/upload", methods=["POST"])
def upload_audio():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    # Parse hearing loss and tuning gain from headers
    hearing_loss = json.loads(request.headers.get("x-hearing-loss", "{}"))
    tuning_gain = request.headers.get("x-tuning-gain", "50")

    fname = file.filename
    in_path = os.path.join(UPLOAD_FOLDER, fname)
    out_name = f"enhanced_{fname.rsplit('.', 1)[0]}.wav"
    out_path = os.path.join(PROCESSED_FOLDER, out_name)

    file.save(in_path)

    # Process using the full chain
    process_audio_with_full_chain(in_path, out_path, hearing_loss, tuning_gain)

    # ---- LAUNCH PREVIEW WINDOW (RE-ADDED) ----
    import subprocess, sys

    print("📊 Launching spectrum preview window...")

    subprocess.Popen([
        sys.executable,
        "preview.py",
        "--input", in_path,
        "--output", out_path,
        "--profile", json.dumps(hearing_loss),
        "--gain_factor", str(float(tuning_gain) / 100.0)
    ])

    return jsonify({
        "message": "processed",
        "processed_file": f"processed/{out_name}"
    })


@app.route("/download/<filename>")
def download_audio(filename):
    return send_from_directory(PROCESSED_FOLDER, filename)


if __name__ == "__main__":
    print("🚀 AAES Backend Running (full processing chain with preview)")
    app.run(debug=True)
