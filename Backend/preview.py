import argparse
import json
import numpy as np
import librosa
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.ndimage import gaussian_filter1d

plt.style.use("default")   # White background theme

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
# Vertical Audiogram Guides
# -----------------------------------------------------
def draw_standard_freq_guides(ax):
    for f in STANDARD_FREQS:
        ax.axvline(x=f, color="#555", linestyle="--", linewidth=0.8)

    ax.set_xticks(STANDARD_FREQS)
    ax.set_xticklabels([str(f) for f in STANDARD_FREQS], fontsize=10, color="black")


# -----------------------------------------------------
# Main UI
# -----------------------------------------------------
def main(args):
    input_path = args.input
    output_path = args.output
    profile = json.loads(args.profile)

    # 2 PANEL LAYOUT (Input + Output Spectrum)
    fig, ax = plt.subplots(2, 1, figsize=(13, 10))

    fig.suptitle("AAES Spectrum Analyzer",
                 fontsize=20, fontweight="bold", color="black")

    fig.patch.set_facecolor("white")
    for axis in ax:
        axis.set_facecolor("white")
        axis.tick_params(colors="black")

    # -----------------------------------------------------
    # Animation Update
    # -----------------------------------------------------
    def update(frame):
        inp = compute_spectrum(input_path)
        out = compute_spectrum(output_path)

        # ------------------ INPUT SPECTRUM ------------------
        if inp:
            f, L, R, sr = inp
            ax[0].clear()
            ax[0].set_xscale("log")
            ax[0].plot(f, L, color="#4fd3ff", linewidth=2, label="Left Input")
            ax[0].plot(f, R, color="#ff4f88", linewidth=2, label="Right Input")
            ax[0].set_xlim([125, 8000])
            ax[0].set_title("Input Spectrum", color="black", fontsize=14)
            ax[0].set_xlabel("Frequency (Hz)", color="black")
            ax[0].set_ylabel("dB", color="black")
            draw_standard_freq_guides(ax[0])
            leg = ax[0].legend(facecolor="white", edgecolor="#777")
            for txt in leg.get_texts(): txt.set_color("black")
            ax[0].tick_params(colors="black")

        # ------------------ OUTPUT SPECTRUM ------------------
        if out:
            f2, L2, R2, sr2 = out
            ax[1].clear()
            ax[1].set_xscale("log")
            ax[1].plot(f2, L2, color="#4fff87", linewidth=2.3, label="Left Output")
            ax[1].plot(f2, R2, color="#ffdd4f", linewidth=2.3, label="Right Output")
            ax[1].set_xlim([125, 8000])
            ax[1].set_title("Output Spectrum (Processed)", color="black", fontsize=14)
            ax[1].set_xlabel("Frequency (Hz)", color="black")
            ax[1].set_ylabel("dB", color="black")
            draw_standard_freq_guides(ax[1])
            leg = ax[1].legend(facecolor="white", edgecolor="#777")
            for txt in leg.get_texts(): txt.set_color("black")
            ax[1].tick_params(colors="black")

    anim = FuncAnimation(fig, update, interval=1000, cache_frame_data=False)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
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
