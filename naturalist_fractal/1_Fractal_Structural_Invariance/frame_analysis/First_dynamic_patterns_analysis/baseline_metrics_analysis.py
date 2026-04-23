import os
import pandas as pd
import matplotlib.pyplot as plt
import json

os.makedirs("csv", exist_ok=True)
os.makedirs("plot_reports", exist_ok=True)
os.makedirs("json_reports", exist_ok=True)

# Load CSV file
file_name = 'csv/frame_analysis_results.csv'
data = pd.read_csv(file_name)

# JSON Report Data
json_report_data = {
    "phase": "Baseline Metrics",
    "name": "Baseline Metrics Analysis",
    "metrics": {
        "frame": data["Frame"].tolist(),
        "avg_intensity": data["Avg Intensity"].tolist(),
        "max_intensity": data["Max Intensity"].tolist(),
        "quantum_coherence": data["Quantum Coherence"].tolist()
    },
    "correlation_matrix": data.corr().to_dict()
}

# Create graphs for each column
plt.figure(figsize=(10, 6))
plt.plot(data['Frame'], data['Avg Intensity'], label='Avg Intensity', color='blue')
plt.plot(data['Frame'], data['Max Intensity'], label='Max Intensity', color='orange')
plt.plot(data['Frame'], data['Quantum Coherence'], label='Quantum Coherence', color='green')
plt.xlabel('Frame')
plt.ylabel('Values')
plt.title('Analysis of Frame Data')
plt.legend()
plt.grid(True)
plt.savefig("plot_reports/frame_data_analysis.png", dpi=150, bbox_inches="tight")
plt.show()

# Save JSON Report
json_report_file = "json_reports/baseline_metrics_analysis.json"
with open(json_report_file, "w", encoding="utf-8") as f:
    json.dump(json_report_data, f, indent=2, ensure_ascii=False)

# Save analysis results
analysis_results = data.describe()
output_file = "csv/analysis_summary.csv"
analysis_results.to_csv(output_file)
print(f"Analysis results saved to {output_file}.")
print(f"JSON report saved to {json_report_file}")
