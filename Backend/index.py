import os
import numpy as np
import soundfile as sf
from scipy.signal import butter, filtfilt, lfilter
from pydub import AudioSegment
from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
import librosa

# Flask App Setup
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

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

# MMSE Noise Reduction
def mmse_filter(audio, sr, noise_estimation_duration=1.0):
    print("🔇 Reducing noise using MMSE")

    if audio.ndim == 2:
        audio_mono = np.mean(audio, axis=0)
    else:
        audio_mono = audio

    noise_samples = int(noise_estimation_duration * sr)
    noise_estimate = audio_mono[:noise_samples]

    stft_audio = librosa.stft(audio_mono)
    stft_noise = librosa.stft(noise_estimate)

    noise_psd = np.mean(np.abs(stft_noise) ** 2, axis=1)
    audio_psd = np.abs(stft_audio) ** 2

    mmse_gain = audio_psd / (audio_psd + noise_psd[:, np.newaxis] + 1e-8)
    filtered_stft = mmse_gain * stft_audio

    denoised_audio_mono = librosa.istft(filtered_stft)

    denoised_audio = np.vstack((denoised_audio_mono, denoised_audio_mono))
    return denoised_audio

# STFT-based Denoising
def stft_denoising(audio, sr):
    print("✨ Applying STFT Denoising")
    D = librosa.stft(audio)
    magnitude, phase = np.abs(D), np.angle(D)
    
    threshold = np.median(magnitude)
    magnitude = np.where(magnitude > threshold, magnitude, 0)
    
    cleaned = magnitude * np.exp(1j * phase)
    return librosa.istft(cleaned)

# Boost High-Pitch Vocals
def high_pitch_boost(audio, sr, boost_db=5, freq=3000):
    print("🎤 Boosting High-Pitch Vocals")
    nyquist = sr / 2
    freq = freq / nyquist
    b, a = butter(2, freq, btype="high")
    boosted = filtfilt(b, a, audio)
    return audio + (boosted * (10 ** (boost_db / 20)))

# LMS Adaptive Filter
def apply_lms_filter(audio, desired=None, mu=0.001, filter_order=32):
    print("🔄 Applying LMS Filter")
    n_samples = len(audio)
    if desired is None:
        desired = audio

    w = np.zeros(filter_order)
    filtered_audio = np.zeros(n_samples)

    for n in range(filter_order, n_samples):
        x = audio[n - filter_order:n][::-1]
        y = np.dot(w, x)
        e = desired[n] - y
        w += 2 * mu * e * x
        filtered_audio[n] = y

    return filtered_audio

# Vocal Boost
def vocal_boost(left, right):
    print("🎙️ Enhancing Vocals")
    left *= 1.15
    right *= 1.15
    return left, right

# Capacitor Effect Simulation
def capacitor_effect(audio, sr, smoothing_factor=0.3):
    print("🔋 Applying Capacitor Effect")
    alpha = smoothing_factor
    return lfilter([alpha], [1, alpha - 1], audio)

# Final Volume Boost
def final_volume_boost(audio):
    print("🔊 Increasing Final Volume")
    return audio * 1.2

# Main Audio Processor
def process_audio(input_path, output_path):
    try:
        print(f"🎧 Processing audio: {input_path}")

        if not input_path.endswith(".wav"):
            input_path = convert_to_wav(input_path)

        left_audio, right_audio, sr = load_audio(input_path)

        left_audio = apply_lms_filter(left_audio)
        right_audio = apply_lms_filter(right_audio)

        left_audio = stft_denoising(left_audio, sr)
        right_audio = stft_denoising(right_audio, sr)

        left_audio = high_pitch_boost(left_audio, sr)
        right_audio = high_pitch_boost(right_audio, sr)

        left_audio, right_audio = vocal_boost(left_audio, right_audio)

        left_audio = capacitor_effect(left_audio, sr)
        right_audio = capacitor_effect(right_audio, sr)

        left_audio, right_audio = match_audio_lengths(left_audio, right_audio)
        stereo_audio = np.vstack((left_audio, right_audio))

        stereo_audio = mmse_filter(stereo_audio, sr)

        final_audio = final_volume_boost(stereo_audio)

        sf.write(output_path, final_audio.T, sr)
        print(f"✅ Processing complete: {output_path}")

    except Exception as e:
        print(f"❌ Processing error: {e}")
        raise ValueError(f"Processing error: {e}")

# Flask Routes
@app.route("/upload", methods=["POST"])
def upload_audio():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "❌ No file uploaded"}), 400

    filename = file.filename
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    processed_filename = f"enhanced_{filename.rsplit('.', 1)[0]}.wav"
    processed_path = os.path.join(PROCESSED_FOLDER, processed_filename)

    try:
        print(f"📁 Saving uploaded file: {file_path}")
        file.save(file_path)
        process_audio(file_path, processed_path)
        processed_url = f"http://127.0.0.1:5000/download/{processed_filename}"
        return jsonify({"message": "✅ File processed successfully", "processed_file": processed_url})
    except Exception as e:
        return jsonify({"error": f"❌ Processing failed: {str(e)}"}), 500

@app.route("/download/<filename>", methods=["GET"])
def download_audio(filename):
    return send_from_directory(PROCESSED_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
