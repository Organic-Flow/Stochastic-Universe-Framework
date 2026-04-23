import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.arima.model import ARIMA
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import json

os.makedirs("csv", exist_ok=True)
os.makedirs("plot_reports", exist_ok=True)
os.makedirs("json_reports", exist_ok=True)


# Load data
data_path = "csv/enhanced_balance_analysis.csv"  # Enter the path to your file
data = pd.read_csv(data_path)

# Convert columns to numeric form (if needed)
numeric_columns = ["Frame", "Avg Intensity", "Balance Index", "Rate_of_Change", "Intensity_Ratio"]
for col in numeric_columns:
    if col in data.columns:  # Check if the column exists
        data[col] = pd.to_numeric(data[col], errors='coerce')

# Create Rate_of_Change column if missing
if "Rate_of_Change" not in data.columns:
    data["Rate_of_Change"] = data["Balance Index"].diff().fillna(0)  # Calculate difference

# Create Intensity_Ratio column if missing
if "Intensity_Ratio" not in data.columns:
    data["Intensity_Ratio"] = data["Avg Intensity"] / data["Avg Intensity"].max()

# Clean data
data = data.dropna()

# Select only numeric columns to calculate correlation matrix
numeric_data = data.select_dtypes(include=[np.number])

# JSON Report Data
json_report_data = {
    "phase": "3.1",
    "name": "ARIMA and Random Forest Analysis",
    "correlation_matrix": numeric_data.corr().to_dict()
}

# 1. Calculate correlation matrix
correlation_matrix = numeric_data.corr()

# Visualize correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
plt.title("Heatmap: Variable Correlations")
plt.savefig("plot_reports/p3.1_correlation_heatmap.png", dpi=150, bbox_inches="tight")
plt.show()

# 2. Time-series analysis (ARIMA)
balance_index = data["Balance Index"]
arima_model = ARIMA(balance_index, order=(1, 1, 1))
arima_result = arima_model.fit()

# ARIMA predictions
predicted_balance = arima_result.predict(start=1, end=len(balance_index), dynamic=False)

# Calculate errors
mse = mean_squared_error(balance_index[1:], predicted_balance[1:])
r2 = r2_score(balance_index[1:], predicted_balance[1:])

json_report_data["arima_fit"] = {
    "frame": data["Frame"].tolist(),
    "actual": balance_index.tolist(),
    "predicted": predicted_balance.tolist(),
    "mse": mse,
    "r2": r2
}

# 3. Random Forest for feature importance
features = numeric_data[["Frame", "Avg Intensity", "Rate_of_Change", "Intensity_Ratio"]]
target = numeric_data["Balance Index"]
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(features, target)

# Feature importance
feature_importances = rf_model.feature_importances_
json_report_data["feature_importances"] = dict(zip(features.columns, feature_importances.tolist()))

# Visualizations
# Time analysis with ARIMA
plt.figure()
plt.plot(data["Frame"], balance_index, label="Actual Balance Index")
plt.plot(data["Frame"], predicted_balance, label="ARIMA Fit", color="red")
plt.title("Time-Lapse: Balance Index")
plt.xlabel("Frame")
plt.ylabel("Balance Index")
plt.legend()
plt.savefig("plot_reports/p3.1_arima_balance_index.png", dpi=150, bbox_inches="tight")
plt.show()

# Feature importance
plt.figure()
sns.barplot(x=feature_importances, y=features.columns)
plt.title("Feature Importance (Random Forest)")
plt.xlabel("Importance")
plt.ylabel("Features")
plt.savefig("plot_reports/p3.1_feature_importances.png", dpi=150, bbox_inches="tight")
plt.show()

# Optimal balance point
optimal_frame = data.loc[rf_model.predict(features).argmax(), "Frame"]
optimal_balance = data.loc[rf_model.predict(features).argmax(), "Balance Index"]

plt.figure()
plt.plot(data["Frame"], balance_index, label="Actual Balance Index")
plt.scatter(optimal_frame, optimal_balance, color="green", label="Optimal Point")
plt.title("Optimal Balance Index")
plt.xlabel("Frame")
plt.ylabel("Balance Index")
plt.legend()
plt.savefig("plot_reports/p3.1_optimal_balance.png", dpi=150, bbox_inches="tight")
plt.show()

json_report_data["optimal_balance"] = {
    "optimal_frame": float(optimal_frame),
    "optimal_balance": float(optimal_balance),
    "data": data[["Frame", "Balance Index"]].to_dict(orient="records")
}

# Print results
print(f"Mean Squared Error (MSE): {mse}")
print(f"R-squared: {r2}")
print(f"Optimal Frame: {optimal_frame}")
print(f"Optimal Balance Index: {optimal_balance}")

# Save JSON Report
json_report_file = "json_reports/p3.1_arima_and_random_forest.json"
with open(json_report_file, "w", encoding="utf-8") as f:
    json.dump(json_report_data, f, indent=2, ensure_ascii=False)
print(f"JSON report saved to {json_report_file}")
