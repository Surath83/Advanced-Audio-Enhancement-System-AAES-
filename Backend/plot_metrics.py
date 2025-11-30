import pandas as pd
import matplotlib.pyplot as plt

# Load your Excel file
df = pd.read_excel("./aaes_reports.xlsx")

# ------------------------
# 1. Plot ΔSNR over experiments
# ------------------------
plt.figure(figsize=(10, 5))
plt.plot(df["delta_snr"], marker='o')
plt.title("ΔSNR Improvement per Test")
plt.xlabel("Test Number")
plt.ylabel("ΔSNR (dB)")
plt.grid(True)
plt.tight_layout()
plt.savefig("delta_snr_plot.png")
plt.close()

# ------------------------
# 2. Plot Latency
# ------------------------
plt.figure(figsize=(10, 5))
plt.plot(df["latency_ms"], marker='o', color="orange")
plt.title("Processing Latency per Test")
plt.xlabel("Test Number")
plt.ylabel("Latency (ms)")
plt.grid(True)
plt.tight_layout()
plt.savefig("latency_plot.png")
plt.close()

# ------------------------
# 3. Plot STOI Score
# ------------------------
plt.figure(figsize=(10, 5))
plt.plot(df["stoi"], marker='o', color="green")
plt.title("STOI Score per Test")
plt.xlabel("Test Number")
plt.ylabel("STOI (0–1)")
plt.grid(True)
plt.tight_layout()
plt.savefig("stoi_plot.png")
plt.close()

# ------------------------
# 4. Plot LSD (log spectral distance)
# ------------------------
plt.figure(figsize=(10, 5))
plt.plot(df["lsd"], marker='o', color="red")
plt.title("LSD per Test")
plt.xlabel("Test Number")
plt.ylabel("LSD")
plt.grid(True)
plt.tight_layout()
plt.savefig("lsd_plot.png")
plt.close()

# ------------------------
# 5. Stereo Energy Balance (L/R)
# ------------------------
plt.figure(figsize=(10, 5))
plt.plot(df["stereo_energy_balance_db"], marker='o', color="purple")
plt.title("Stereo Energy Balance per Test")
plt.xlabel("Test Number")
plt.ylabel("L/R Balance (dB)")
plt.grid(True)
plt.tight_layout()
plt.savefig("stereo_balance_plot.png")
plt.close()
