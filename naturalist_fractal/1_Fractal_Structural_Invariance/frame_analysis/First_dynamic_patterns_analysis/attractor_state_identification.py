import os
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("csv", exist_ok=True)
os.makedirs("plot_reports", exist_ok=True)

# Load the data
file_path = "csv/frame_analysis_results.csv"
data = pd.read_csv(file_path)

# Normalize column names
data.columns = data.columns.str.strip()

# Calculate basic statistics
data["Quantum Coherence Variance"] = data["Quantum Coherence"].rolling(window=10, min_periods=1).std()

# New analysis criteria
high_energy_threshold = data["Avg Intensity"].quantile(0.85)
low_variance_threshold = data["Quantum Coherence Variance"].quantile(0.15)

# Identify frames based on new criteria
high_energy_frames = data[data["Avg Intensity"] >= high_energy_threshold]
low_variance_frames = data[data["Quantum Coherence Variance"] <= low_variance_threshold]
selected_frames = pd.merge(high_energy_frames, low_variance_frames, on="Frame", suffixes=('', '_drop'))
selected_frames = selected_frames[[c for c in selected_frames.columns if not c.endswith('_drop')]]

# Verification
if selected_frames.empty:
    print("No frames matched the criteria. Adjust the thresholds and retry.")
else:
    print(f"Selected frames: {len(selected_frames)}")

# Visualize results
plt.figure(figsize=(12, 6))
plt.plot(data["Frame"], data["Avg Intensity"], label="Avg Intensity", color="blue", alpha=0.7)
plt.scatter(high_energy_frames["Frame"], high_energy_frames["Avg Intensity"], label="High Energy Frames", color="red", s=10)
plt.scatter(low_variance_frames["Frame"], low_variance_frames["Avg Intensity"], label="Low Variance Frames", color="green", s=10)
plt.scatter(selected_frames["Frame"], selected_frames["Avg Intensity"], label="Selected Frames", color="purple", s=15)
plt.title("Analysis of Frames for Energy and Balance")
plt.xlabel("Frame")
plt.ylabel("Avg Intensity")
plt.legend()
plt.grid()
plt.savefig("plot_reports/attractor_state_identification.png", dpi=150, bbox_inches="tight")
plt.show()

# Save results
selected_frames.to_csv("csv/selected_frames_analysis.csv", index=False)
print("Analysis results saved in 'csv/selected_frames_analysis.csv'.")
