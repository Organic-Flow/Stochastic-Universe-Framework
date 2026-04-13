import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from mpl_toolkits.mplot3d import Axes3D

os.makedirs("csv", exist_ok=True)
os.makedirs("plot_reports", exist_ok=True)


# Read the CSV file
csv_file = "csv/ideal_frames_analysis.csv"
df = pd.read_csv(csv_file)

# Exclude the "Folder" column before calculating correlations
numeric_df = df.select_dtypes(include=[np.number])

# Review statistical features
print("Statistical features:")
print(df.describe())

# Extract Ideal Frames (Based on Avg Intensity and Max Intensity)
ideal_frames = df[(df["Avg Intensity"] > 0.7) & (df["Max Intensity"] == 1.0)]
print(f"Number of ideal frames: {len(ideal_frames)}")

# Distribution of Average and Maximum Intensity
plt.figure(figsize=(8, 6))
sns.kdeplot(df["Avg Intensity"], label="Avg Intensity", fill=True, color="blue")
sns.histplot(df["Max Intensity"], label="Max Intensity", fill=True, color="red", alpha=0.6, bins=10)
plt.title("Distribution of Average and Maximum Intensity")
plt.xlabel("Intensity")
plt.ylabel("Count")
plt.legend()
plt.savefig("plot_reports/p2.1_intensity_distribution.png", dpi=150, bbox_inches="tight")
plt.show()

# Heatmap for correlations (numeric columns only)
plt.figure(figsize=(8, 6))
correlation_matrix = numeric_df.corr()  # Use numeric_df instead of the whole df
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Variable Correlations")
plt.savefig("plot_reports/p2.1_correlation_heatmap.png", dpi=150, bbox_inches="tight")
plt.show()

# 3D Visualization for Energy (Frame vs Avg Intensity vs Max Intensity)
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df["Frame"], df["Avg Intensity"], df["Max Intensity"], c=df["Avg Intensity"], cmap="viridis", s=20)
ax.set_xlabel("Frame")
ax.set_ylabel("Avg Intensity")
ax.set_zlabel("Max Intensity")
plt.title("3D Visualization: Frame vs Avg Intensity vs Max Intensity")
plt.savefig("plot_reports/p2.1_3d_frame_intensity.png", dpi=150, bbox_inches="tight")
plt.show()

# Modeling for Balance Equation (using regression)
X = numeric_df[["Frame", "Avg Intensity"]]
y = numeric_df["Max Intensity"]
model = LinearRegression()
model.fit(X, y)

# Coefficients and Equation
coef = model.coef_
intercept = model.intercept_
print(f"Balance Equation: Max Intensity = {coef[0]:.3f}*Frame + {coef[1]:.3f}*Avg Intensity + {intercept:.3f}")

# Predictions and visualization
df["Predicted Max Intensity"] = model.predict(X)
plt.figure(figsize=(8, 6))
plt.scatter(df["Frame"], df["Max Intensity"], label="Actual", alpha=0.6)
plt.scatter(df["Frame"], df["Predicted Max Intensity"], label="Predicted", alpha=0.6, color="red")
plt.title("Actual vs Predicted Maximum Intensity")
plt.xlabel("Frame")
plt.ylabel("Max Intensity")
plt.legend()
plt.savefig("plot_reports/p2.1_linear_regression_fit.png", dpi=150, bbox_inches="tight")
plt.show()

# Save the updated CSV
df.to_csv("csv/final_analysis_with_predictions.csv", index=False)
print("Analysis completed. Data saved to final_analysis_with_predictions.csv.")
