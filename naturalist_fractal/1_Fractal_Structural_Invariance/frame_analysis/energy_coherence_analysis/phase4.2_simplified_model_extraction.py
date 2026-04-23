import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
import json

os.makedirs("csv", exist_ok=True)
os.makedirs("plot_reports", exist_ok=True)
os.makedirs("json_reports", exist_ok=True)


# Load data
df = pd.read_csv('csv/enhanced_balance_analysis.csv')

# Preprocessing: Select simple features
# Max Intensity is constant, but we include it as requested for the "minimal description"
X = df[['Max Intensity', 'Frame', 'Avg Intensity']]
y = df['Balance Index']

# JSON Report Data
json_report_data = {
    "phase": "4.2",
    "name": "Simplified Model Extraction",
}

# Gradient Boosting Regressor (Simplified)
gb_model = GradientBoostingRegressor(n_estimators=50, learning_rate=0.1, max_depth=2, random_state=42)
gb_model.fit(X, y)
gb_preds = gb_model.predict(X)

mse = mean_squared_error(y, gb_preds)
r2 = r2_score(y, gb_preds)
print(f"Simplified GBR Mean Squared Error: {mse:.7f}")
print(f"Simplified GBR R-squared: {r2:.7f}")

json_report_data["simplified_results"] = {
    "mse": mse,
    "r2": r2,
    "predictions": gb_preds.tolist()
}

# Feature Importance
feature_importances = gb_model.feature_importances_
importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': feature_importances})
importance_df = importance_df.sort_values(by='Importance', ascending=False)
json_report_data["feature_importances"] = importance_df.to_dict(orient="records")

# Information Identity Extraction
print("\nInformation Identity (Variance Contribution):")
for idx, row in importance_df.iterrows():
    print(f"{row['Feature']}: {row['Importance']*100:.4f}%")

# Visualization: Feature Importance
plt.figure(figsize=(10, 6))
sns.barplot(x='Importance', y='Feature', data=importance_df)
plt.title('Feature Importance (Simplified GBR) - Information Identity')
plt.savefig("plot_reports/p4.2_feature_importances.png", dpi=150, bbox_inches="tight")
plt.show()

# Visualization: Actual vs Predicted
plt.figure(figsize=(12, 6))
plt.scatter(df['Frame'], y, label='Actual Balance Index', color='blue', alpha=0.6)
plt.plot(df['Frame'], gb_preds, label='Simplified GBR Fit', color='orange', linewidth=2)
plt.title('Simplified GBR Fit: Balance Index vs Frame')
plt.xlabel('Frame')
plt.ylabel('Balance Index')
plt.legend()
plt.savefig("plot_reports/p4.2_simplified_predictions.png", dpi=150, bbox_inches="tight")
plt.show()

json_report_data["actual_vs_predicted"] = {
    "frame": df["Frame"].tolist(),
    "actual": y.tolist(),
    "predicted": gb_preds.tolist()
}

# Save JSON Report
json_report_file = "json_reports/p4.2_simplified_model_extraction.json"
with open(json_report_file, "w", encoding="utf-8") as f:
    json.dump(json_report_data, f, indent=2, ensure_ascii=False)

# Save results
df['Simplified_GBR_Predictions'] = gb_preds
df.to_csv('csv/simplified_model_results.csv', index=False)
print("Analysis completed. Data saved to simplified_model_results.csv.")
print(f"JSON report saved to {json_report_file}")
