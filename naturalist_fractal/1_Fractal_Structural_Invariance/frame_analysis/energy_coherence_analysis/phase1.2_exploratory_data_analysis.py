import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # For prettier graphs, install with `pip install seaborn`
import json

os.makedirs("csv", exist_ok=True)
os.makedirs("plot_reports", exist_ok=True)
os.makedirs("json_reports", exist_ok=True)


# Load CSV
csv_file = "csv/new_frame_analysis.csv"
df = pd.read_csv(csv_file)

# Overview of data
print("First lines of file:")
print(df.head())

print("\nStatistical data:")
print(df.describe())

# Data for JSON Report
json_report_data = {
    "phase": "1.2",
    "name": "Exploratory Data Analysis",
    "intensity_distribution": {
        "avg": df["Avg Intensity"].tolist(),
        "max": df["Max Intensity"].tolist()
    },
    "avg_vs_max_scatter": df[["Avg Intensity", "Max Intensity", "Folder"]].to_dict(orient="records"),
    "intensity_by_folder": {
        folder: df[df["Folder"] == folder]["Avg Intensity"].tolist()
        for folder in df["Folder"].unique()
    }
}

# Analysis of average and maximum intensity
plt.figure(figsize=(10, 6))
sns.histplot(df["Avg Intensity"], kde=True, bins=30, color="blue", label="Avg Intensity")
sns.histplot(df["Max Intensity"], kde=True, bins=30, color="red", label="Max Intensity")
plt.title("Distribution of Average and Maximum Intensity")
plt.xlabel("Intensity")
plt.ylabel("Count")
plt.legend()
plt.savefig("plot_reports/p1.2_intensity_distribution.png", dpi=150, bbox_inches="tight")
plt.show()

# Relationship between Average and Maximum Intensity
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x="Avg Intensity", y="Max Intensity", hue="Folder", palette="viridis")
plt.title("Relationship between Average and Maximum Intensity")
plt.xlabel("Avg Intensity")
plt.ylabel("Max Intensity")
plt.legend(title="Folder", loc="upper right")
plt.savefig("plot_reports/p1.2_avg_vs_max_scatter.png", dpi=150, bbox_inches="tight")
plt.show()

# Analysis of intensity per folder
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x="Folder", y="Avg Intensity", palette="coolwarm")
plt.title("Average Intensity Per Folder")
plt.xlabel("Folder")
plt.ylabel("Avg Intensity")
plt.savefig("plot_reports/p1.2_intensity_by_folder.png", dpi=150, bbox_inches="tight")
plt.show()

# Detection of ideal states: Maximum intensity with balance
threshold_avg = df["Avg Intensity"].quantile(0.9)  # Define threshold for high average intensity
ideal_frames = df[(df["Avg Intensity"] > threshold_avg) & (df["Max Intensity"] > 0.95)]

print(f"Number of ideal frames: {len(ideal_frames)}")
print("Ideal Frames:")
print(ideal_frames)

# Visualization of ideal states
plt.figure(figsize=(8, 6))
sns.scatterplot(data=ideal_frames, x="Frame", y="Avg Intensity", color="purple", label="Ideal Frames")
plt.title("Ideal Frames Based on Intensity")
plt.xlabel("Frame")
plt.ylabel("Avg Intensity")
plt.legend()
plt.savefig("plot_reports/p1.2_ideal_frames.png", dpi=150, bbox_inches="tight")
plt.show()

# Add ideal frames to JSON
json_report_data["ideal_frames"] = ideal_frames[["Frame", "Avg Intensity"]].to_dict(orient="records")

# Save JSON Report
json_report_file = "json_reports/p1.2_exploratory_data_analysis.json"
with open(json_report_file, "w", encoding="utf-8") as f:
    json.dump(json_report_data, f, indent=2, ensure_ascii=False)

# Save ideal frames to new file
ideal_csv = "csv/ideal_frames_analysis.csv"
ideal_frames.to_csv(ideal_csv, index=False)
print(f"Ideal frames were saved to {ideal_csv}")
print(f"JSON report saved to {json_report_file}")
