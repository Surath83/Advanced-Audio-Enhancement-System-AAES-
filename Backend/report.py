# report.py
import json
import numpy as np
import librosa
import pandas as pd
import os

# ---- SAFE IMPORTS ----
try:
    from pystoi import stoi
except ImportError:
    print("⚠️ pystoi not installed — STOI metric will be skipped.")
    stoi = None

try:
    from pesq import pesq
except ImportError:
    print("⚠️ pesq not installed — PESQ metric will be skipped.")
    pesq = None



CSV_FILE = "aaes_reports.csv"  

def append_report_to_csv(report_data):
    """
    Append report metrics to a CSV file.
    Creates header automatically if file doesn't exist.
    """

    # Flatten JSON structure
    row = {
        "hearing_loss": json.dumps(report_data["hearing_loss"]),
        "tuning_gain_percent": report_data["tuning_gain_percent"],
        "sample_rate": report_data["sample_rate"],
        "latency_ms": report_data["latency_ms"],

        "snr_before": report_data["metrics"]["snr_before"],
        "snr_after": report_data["metrics"]["snr_after"],
        "delta_snr": report_data["metrics"]["delta_snr"],

        "pesq": report_data["metrics"]["pesq"],
        "stoi": report_data["metrics"]["stoi"],
        "lsd": report_data["metrics"]["lsd"],
        "stereo_energy_balance_db": report_data["metrics"]["stereo_energy_balance_db"],
    }

    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())

        # Create header only once
        if not file_exists:
            writer.writeheader()

        writer.writerow(row)

    print(f"📈 CSV updated: {CSV_FILE}")

# ---------- Utility Functions ----------
def compute_snr(clean, enhanced):
    noise = clean - enhanced
    snr = 10 * np.log10(np.sum(clean ** 2) / (np.sum(noise ** 2) + 1e-10))
    return float(snr)


def compute_lsd(clean, enhanced):
    eps = 1e-9
    stft_clean = np.abs(librosa.stft(clean)) + eps
    stft_enhanced = np.abs(librosa.stft(enhanced)) + eps
    lsd = np.mean(np.sqrt(np.mean((20 * np.log10(stft_clean/stft_enhanced)) ** 2, axis=0)))
    return float(lsd)


def stereo_energy_balance(left, right):
    L_energy = np.sum(left ** 2)
    R_energy = np.sum(right ** 2)
    if R_energy == 0:
        return "Undefined"
    balance_db = 10 * np.log10(L_energy / R_energy)
    return float(balance_db)


# ---------- Main Report Generator ----------
def generate_report(original_audio, enhanced_audio, sr, hearing_loss, tuning_gain, latency_ms):

    orig_mono = np.mean(original_audio, axis=0)
    enh_mono = np.mean(enhanced_audio, axis=0)

    # 1. SNR
    snr_before = compute_snr(orig_mono, orig_mono)
    snr_after = compute_snr(orig_mono, enh_mono)
    delta_snr = snr_after - snr_before

    # 2. PESQ
    if pesq:
        try:
            pesq_score = pesq(sr, orig_mono, enh_mono, 'wb')
        except:
            pesq_score = None
    else:
        pesq_score = None


    # 3. STOI
    if stoi:
        try:
            stoi_score = stoi(orig_mono, enh_mono, sr, extended=False)
        except:
            stoi_score = None
    else:
        stoi_score = None


    # 4. LSD
    lsd_value = compute_lsd(orig_mono, enh_mono)

    # 5. Stereo balance
    seb = stereo_energy_balance(enhanced_audio[0], enhanced_audio[1])

    # Final dict
    return {
        "hearing_loss": hearing_loss,
        "tuning_gain_percent": tuning_gain,
        "sample_rate": sr,
        "latency_ms": latency_ms,

        "metrics": {
            "snr_before": snr_before,
            "snr_after": snr_after,
            "delta_snr": delta_snr,
            "pesq": pesq_score,
            "stoi": stoi_score,
            "lsd": lsd_value,
            "stereo_energy_balance_db": seb
        }
    }


EXCEL_FILE = "aaes_reports.xlsx"

def append_report_to_excel(report):
    """
    Appends the current report into aaes_reports.xlsx.
    Automatically creates file and header if missing.
    """

    # Flatten dictionary for Excel row
    row = {
        "hearing_loss": json.dumps(report["hearing_loss"]),
        "tuning_gain_percent": report["tuning_gain_percent"],
        "sample_rate": report["sample_rate"],
        "latency_ms": report["latency_ms"],
        "snr_before": report["metrics"]["snr_before"],
        "snr_after": report["metrics"]["snr_after"],
        "delta_snr": report["metrics"]["delta_snr"],
        "pesq": report["metrics"].get("pesq"),
        "stoi": report["metrics"].get("stoi"),
        "lsd": report["metrics"]["lsd"],
        "stereo_energy_balance_db": report["metrics"]["stereo_energy_balance_db"],
    }

    # Convert to DataFrame
    df_new = pd.DataFrame([row])

    # If file exists → append
    if os.path.isfile(EXCEL_FILE):
        df_existing = pd.read_excel(EXCEL_FILE)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new

    # Save back to Excel
    df_combined.to_excel(EXCEL_FILE, index=False)

    print(f"📘 Excel updated: {EXCEL_FILE}")
