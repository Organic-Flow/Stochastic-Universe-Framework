import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import json

os.makedirs("csv", exist_ok=True)
os.makedirs("plot_reports", exist_ok=True)
os.makedirs("json_reports", exist_ok=True)

# Load the CSV file
file_path = "csv/final_analysis_with_predictions.csv"
df = pd.read_csv(file_path)

# Extract statistical features
print("Statistical features:")
print(df.describe())

# Focus on ideal frames
ideal_frames = df[df["Avg Intensity"] > 0.75]
print(f"Number of ideal frames: {len(ideal_frames)}")

# Correlations between variables
correlation_matrix = df[["Frame", "Avg Intensity", "Max Intensity"]].corr()
print("Variable correlations:")
print(correlation_matrix)

# JSON Report Data
json_report_data = {
    "phase": "2.2",
    "name": "Polynomial Energy Modeling",
    "correlation_matrix": correlation_matrix.to_dict(),
    "intensity_distribution": {
        "avg": df["Avg Intensity"].tolist(),
        "max": df["Max Intensity"].tolist()
    },
    "3d_visualization": df[["Frame", "Avg Intensity", "Max Intensity"]].to_dict(orient="records")
}

# Visualize correlations
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Variable Correlations")
plt.savefig("plot_reports/p2.2_correlation_heatmap.png", dpi=150, bbox_inches="tight")
plt.show()

# Polynomial Regression for Energy
X = df[["Frame", "Avg Intensity"]]
y = df["Max Intensity"]

# Transform features to polynomial
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)

# Model training
model = LinearRegression()
model.fit(X_poly, y)

# Predictions
y_pred = model.predict(X_poly)

# Model Evaluation
mse = mean_squared_error(y, y_pred)
r2 = r2_score(y, y_pred)
print(f"Mean Squared Error (MSE): {mse:.5f}")
print(f"R-squared (R2): {r2:.5f}")

# Add polynomial fit to JSON
json_report_data["polynomial_fit"] = {
    "frame": df["Frame"].tolist(),
    "actual": y.tolist(),
    "predicted": y_pred.tolist(),
    "mse": mse,
    "r2": r2
}

# Model Equation
print("Model Coefficients:", model.coef_)
print("Intercept:", model.intercept_)

# Visualization: Actual vs Predicted Intensity
plt.figure(figsize=(8, 6))
plt.scatter(df["Frame"], y, color="blue", label="Actual", alpha=0.6)
plt.scatter(df["Frame"], y_pred, color="red", label="Predicted", alpha=0.6)
plt.title("Actual vs Predicted Maximum Intensity")
plt.xlabel("Frame")
plt.ylabel("Max Intensity")
plt.legend()
plt.savefig("plot_reports/p2.2_polynomial_fit.png", dpi=150, bbox_inches="tight")
plt.show()

# 3D Visualization: Frame, Avg Intensity, Max Intensity
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(df["Frame"], df["Avg Intensity"], df["Max Intensity"], c=df["Avg Intensity"], cmap="viridis", s=50)
ax.set_title("3D Visualization: Frame vs Avg Intensity vs Max Intensity")
ax.set_xlabel("Frame")
ax.set_ylabel("Avg Intensity")
ax.set_zlabel("Max Intensity")
fig.colorbar(scatter, ax=ax, label="Avg Intensity")
plt.savefig("plot_reports/p2.2_3d_visualization.png", dpi=150, bbox_inches="tight")
plt.show()

# Visualize Distributions
plt.figure(figsize=(8, 6))
sns.histplot(df["Avg Intensity"], kde=True, color="blue", label="Avg Intensity", bins=20)
sns.histplot(df["Max Intensity"], kde=True, color="red", label="Max Intensity", bins=20)
plt.title("Distribution of Average and Maximum Intensity")
plt.xlabel("Intensity")
plt.ylabel("Count")
plt.legend()
plt.savefig("plot_reports/p2.2_intensity_distribution.png", dpi=150, bbox_inches="tight")
plt.show()

# Save JSON Report
json_report_file = "json_reports/p2.2_polynomial_energy_modeling.json"
with open(json_report_file, "w", encoding="utf-8") as f:
    json.dump(json_report_data, f, indent=2, ensure_ascii=False)

# Save results
df["Predicted Max Intensity"] = y_pred
df.to_csv("csv/enhanced_analysis_with_predictions.csv", index=False)
print("Analysis completed. Data saved to enhanced_analysis_with_predictions.csv.")
print(f"JSON report saved to {json_report_file}")
