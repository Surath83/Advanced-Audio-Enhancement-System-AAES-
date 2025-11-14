import argparse
import json
import numpy as np
import librosa
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.ndimage import gaussian_filter1d

plt.style.use("seaborn-v0_8-darkgrid")

STANDARD_FREQS = [125, 250, 500, 1000, 2000, 4000, 8000]


# -----------------------------------------------------
# Spectrum Computation
# -----------------------------------------------------
def compute_spectrum(path):
    try:
        y, sr = librosa.load(path, sr=None, mono=False)
    except:
        return None

    # Ensure stereo
    if y.ndim == 1:
        y = np.vstack((y, y))

    L, R = y[0], y[1]

    # STFT
    S_L = np.abs(librosa.stft(L))
    S_R = np.abs(librosa.stft(R))

    # Frequency bins
    freqs = np.linspace(0, sr / 2, S_L.shape[0])
    mask = freqs <= 8000
    freqs = freqs[mask]

    # dB conversion + smoothing
    db_L = 20 * np.log10(np.maximum(S_L.mean(axis=1)[mask], 1e-8))
    db_R = 20 * np.log10(np.maximum(S_R.mean(axis=1)[mask], 1e-8))
    db_L = gaussian_filter1d(db_L, sigma=2)
    db_R = gaussian_filter1d(db_R, sigma=2)

    return freqs, db_L, db_R, sr


# -----------------------------------------------------
# Spectrogram for Heatmap
# -----------------------------------------------------
def compute_spectrogram(path):
    try:
        y, sr = librosa.load(path, sr=None)
    except:
        return None

    # STFT -> Spectrogram
    S = np.abs(librosa.stft(y, n_fft=1024, hop_length=256))
    S_db = librosa.amplitude_to_db(S, ref=np.max)

    return S_db, sr


# -----------------------------------------------------
# Vertical Audiogram Guides
# -----------------------------------------------------
def draw_standard_freq_guides(ax):
    for f in STANDARD_FREQS:
        ax.axvline(x=f, color="#777", linestyle="--", linewidth=0.8)

    ax.set_xticks(STANDARD_FREQS)
    ax.set_xticklabels([str(f) for f in STANDARD_FREQS], fontsize=10, color="white")


# -----------------------------------------------------
# Main UI
# -----------------------------------------------------
def main(args):
    input_path = args.input
    output_path = args.output
    profile = json.loads(args.profile)

    # 3 PANEL LAYOUT:
    # 1. Input Spectrum
    # 2. Output Spectrum
    # 3. Spectrogram Heatmap
    fig, ax = plt.subplots(3, 1, figsize=(13, 12))
    fig.suptitle("AAES Spectrum + Spectrogram Analyzer",
                 fontsize=20, fontweight="bold", color="white")

    fig.patch.set_facecolor("#1b1b1b")
    for axis in ax:
        axis.set_facecolor("#141414")
        axis.tick_params(colors="white")

    # -----------------------------------------------------
    # Animation Update
    # -----------------------------------------------------
    def update(frame):
        inp = compute_spectrum(input_path)
        out = compute_spectrum(output_path)
        spec = compute_spectrogram(output_path)

        # ------------------ INPUT SPECTRUM ------------------
        if inp:
            f, L, R, sr = inp
            ax[0].clear()
            ax[0].set_xscale("log")
            ax[0].plot(f, L, color="#4fd3ff", linewidth=2, label="Left Input")
            ax[0].plot(f, R, color="#ff4f88", linewidth=2, label="Right Input")
            ax[0].set_xlim([125, 8000])
            ax[0].set_title("Input Spectrum", color="white", fontsize=14)
            ax[0].set_xlabel("Frequency (Hz)", color="white")
            ax[0].set_ylabel("dB", color="white")
            draw_standard_freq_guides(ax[0])
            leg = ax[0].legend(facecolor="#222", edgecolor="#555")
            for txt in leg.get_texts(): txt.set_color("white")

        # ------------------ OUTPUT SPECTRUM ------------------
        if out:
            f2, L2, R2, sr2 = out
            ax[1].clear()
            ax[1].set_xscale("log")
            ax[1].plot(f2, L2, color="#4fff87", linewidth=2.3, label="Left Output")
            ax[1].plot(f2, R2, color="#ffdd4f", linewidth=2.3, label="Right Output")
            ax[1].set_xlim([125, 8000])
            ax[1].set_title("Output Spectrum (Processed)", color="white", fontsize=14)
            ax[1].set_xlabel("Frequency (Hz)", color="white")
            ax[1].set_ylabel("dB", color="white")
            draw_standard_freq_guides(ax[1])
            leg = ax[1].legend(facecolor="#222", edgecolor="#555")
            for txt in leg.get_texts(): txt.set_color("white")

        # ------------------ DIFFERENCE HEATMAP (BEFORE vs AFTER) ------------------
        if inp and out:
            # Compute difference between processed and input spectrograms
            S_db_in, sr_s1 = compute_spectrogram(input_path)
            S_db_out, sr_s2 = compute_spectrogram(output_path)

            # Resize to smallest matching shape
            min_rows = min(S_db_in.shape[0], S_db_out.shape[0])
            min_cols = min(S_db_in.shape[1], S_db_out.shape[1])

            S_db_in = S_db_in[:min_rows, :min_cols]
            S_db_out = S_db_out[:min_rows, :min_cols]

            # Δ Heatmap
            diff = S_db_out - S_db_in

            ax[2].clear()
            img = ax[2].imshow(
                diff,
                aspect="auto",
                origin="lower",
                cmap="coolwarm",     # Red = boost, Blue = reduction
            )

            ax[2].set_title("Δ Spectrogram (Processed – Original)", color="white", fontsize=14)
            ax[2].set_xlabel("Time Frames", color="white")
            ax[2].set_ylabel("Frequency Bins", color="white")

            cbar = plt.colorbar(img, ax=ax[2])
            cbar.ax.yaxis.set_tick_params(color="white")
            plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')


    # Run animation
    anim = FuncAnimation(fig, update, interval=1000, cache_frame_data=False)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()


# -----------------------------------------------------
# CLI Entry
# -----------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input")
    parser.add_argument("--output")
    parser.add_argument("--profile")
    parser.add_argument("--gain_factor")
    args = parser.parse_args()

    main(args)
