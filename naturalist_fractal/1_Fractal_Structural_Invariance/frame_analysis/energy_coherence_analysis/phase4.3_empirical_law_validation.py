import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import r2_score, mean_squared_error
import json

os.makedirs("csv", exist_ok=True)
os.makedirs("plot_reports", exist_ok=True)
os.makedirs("json_reports", exist_ok=True)


# Load data
df = pd.read_csv('csv/enhanced_balance_analysis.csv')

# Empirical Law Validation:
# Treating feature importances from GBR as scalar multipliers in a linear formula
# (This is expected to fail with high negative R2 as a mathematical proof)
coeff_avg = 0.999979
coeff_frame = 0.000021

df['Empirical_Law_Balance'] = coeff_avg * df['Avg Intensity'] + coeff_frame * df['Frame']

# Evaluation
y_actual = df['Balance Index']
y_pred = df['Empirical_Law_Balance']
mse = mean_squared_error(y_actual, y_pred)
r2 = r2_score(y_actual, y_pred)

print(f"Empirical Law MSE: {mse:.7f}")
print(f"Empirical Law R-squared: {r2:.7f}")

# JSON Report Data
json_report_data = {
    "phase": "4.3",
    "name": "Empirical Law Validation",
    "validation_results": {
        "mse": mse,
        "r2": r2,
        "frame": df["Frame"].tolist(),
        "actual": y_actual.tolist(),
        "empirical_law_pred": y_pred.tolist()
    }
}

# Visualization: Empirical Law Fit
plt.figure(figsize=(12, 6))
plt.scatter(df['Frame'], y_actual, label='Actual Balance Index', color='blue', alpha=0.6)
plt.plot(df['Frame'], y_pred, label='Empirical Law (Linear Expansion)', color='purple', linewidth=2)
plt.title('Empirical Law Validation: Linear Assumption Check')
plt.xlabel('Frame')
plt.ylabel('Balance Index')
plt.legend()
plt.savefig("plot_reports/p4.3_empirical_law_fit.png", dpi=150, bbox_inches="tight")
plt.show()

# 4. Feature Importance Comparison (for visualization only)
importance_df = pd.DataFrame({'Feature': ['Avg Intensity', 'Frame'], 'Importance': [coeff_avg, coeff_frame]})
plt.figure(figsize=(10, 6))
sns.barplot(x='Importance', y='Feature', data=importance_df)
plt.title('Feature Importances (The Information Identity)')
plt.savefig("plot_reports/p4.3_feature_importances.png", dpi=150, bbox_inches="tight")
plt.show()

json_report_data["feature_importances"] = importance_df.to_dict(orient="records")

# Save JSON Report
json_report_file = "json_reports/p4.3_empirical_law_validation.json"
with open(json_report_file, "w", encoding="utf-8") as f:
    json.dump(json_report_data, f, indent=2, ensure_ascii=False)

# Save results
df.to_csv('csv/empirical_law_results.csv', index=False)
print("Analysis completed. Data saved to empirical_law_results.csv.")
print(f"JSON report saved to {json_report_file}")
