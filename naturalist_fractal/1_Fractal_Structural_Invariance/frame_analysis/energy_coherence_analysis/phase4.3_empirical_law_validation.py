import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score

os.makedirs("csv", exist_ok=True)
os.makedirs("plot_reports", exist_ok=True)


# Load data
data = pd.read_csv("csv/enhanced_balance_analysis.csv")

# Simplified equation based on Gradient Boosting
# Equation: Balance Index = 0.014439 * Avg Intensity + 0.002000 * (Avg Intensity^2) + 0.024495 * (Avg Intensity^3) + 0.000009 * (Frame^2 Avg Intensity)
data['Predicted_Balance_Index'] = (
    0.014439 * data['Avg Intensity'] +
    0.002000 * (data['Avg Intensity'] ** 2) +
    0.024495 * (data['Avg Intensity'] ** 3) +
    0.000009 * (data['Frame'] ** 2 * data['Avg Intensity'])
)

# Calculate MSE and R²
mse = mean_squared_error(data['Balance Index'], data['Predicted_Balance_Index'])
r2 = r2_score(data['Balance Index'], data['Predicted_Balance_Index'])

print(f"Simplified Equation - MSE: {mse}")
print(f"Simplified Equation - R^2: {r2}")

# Visualize Actual and Predicted Values
plt.figure(figsize=(10, 6))
plt.plot(data.index, data['Balance Index'], label='Actual Balance Index', color='blue')
plt.plot(data.index, data['Predicted_Balance_Index'], label='Predicted Balance Index', color='orange', linestyle='dashed')
plt.title("Actual vs Predicted Balance Index")
plt.xlabel("Samples")
plt.ylabel("Balance Index")
plt.legend()
plt.grid()
plt.savefig("plot_reports/p4.3_empirical_law_fit.png", dpi=150, bbox_inches="tight")
plt.show()

# Visualize Variable Importance
features = ['Avg Intensity', 'Avg Intensity^2', 'Avg Intensity^3', 'Frame^2 Avg Intensity']
importances = [0.014439, 0.002000, 0.024495, 0.000009]
plt.figure(figsize=(10, 6))
plt.bar(features, importances, color='blue')
plt.title("Variable Importance (Simplified Equation)")
plt.xlabel("Variables")
plt.ylabel("Importance")
plt.xticks(rotation=45)
plt.grid()
plt.savefig("plot_reports/p4.3_feature_importances.png", dpi=150, bbox_inches="tight")
plt.show()
