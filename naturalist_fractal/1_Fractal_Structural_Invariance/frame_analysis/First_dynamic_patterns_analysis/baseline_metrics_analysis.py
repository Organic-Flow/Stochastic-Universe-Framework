import os
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("csv", exist_ok=True)
os.makedirs("plot_reports", exist_ok=True)

# Load CSV file
file_name = 'csv/frame_analysis_results.csv'
data = pd.read_csv(file_name)

# Display basic information
print("First lines of file:")
print(data.head())

# Calculate basic statistics
print("\nStatistical data:")
print(data.describe())

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

# Correlation between columns
print("\nCorrelation between values:")
print(data.corr())

# Analysis of exceptionally high or low values
high_intensity = data[data['Max Intensity'] > 0.99]
print("\nFrames with maximum intensity > 0.99:")
print(high_intensity)

# Save analysis results
analysis_results = data.describe()
output_file = "csv/analysis_summary.csv"
analysis_results.to_csv(output_file)
print(f"\nAnalysis results were saved to {output_file}.")
