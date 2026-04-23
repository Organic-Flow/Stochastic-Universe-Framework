import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures
import json

os.makedirs("csv", exist_ok=True)
os.makedirs("plot_reports", exist_ok=True)
os.makedirs("json_reports", exist_ok=True)


# Load data
df = pd.read_csv('csv/enhanced_balance_analysis.csv')

# Preprocessing: Polynomial terms for feature expansion
X = df[['Frame', 'Avg Intensity']]
poly = PolynomialFeatures(degree=3, include_bias=False)
X_poly = poly.fit_transform(X)
poly_feature_names = poly.get_feature_names_out(X.columns)

y = df['Balance Index']

# JSON Report Data
json_report_data = {
    "phase": "4.1",
    "name": "Gradient Boosting Equation Extraction",
}

# 1. Gradient Boosting Regressor
gb_model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
gb_model.fit(X_poly, y)
gb_preds = gb_model.predict(X_poly)

gb_mse = mean_squared_error(y, gb_preds)
gb_r2 = r2_score(y, gb_preds)
print(f"GBR Mean Squared Error: {gb_mse:.5f}")
print(f"GBR R-squared: {gb_r2:.5f}")

json_report_data["gbr_results"] = {
    "mse": gb_mse,
    "r2": gb_r2,
    "predictions": gb_preds.tolist()
}

# 2. Neural Network (MLP)
mlp_model = MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=1000, random_state=42)
mlp_model.fit(X_poly, y)
mlp_preds = mlp_model.predict(X_poly)

mlp_mse = mean_squared_error(y, mlp_preds)
mlp_r2 = r2_score(y, mlp_preds)
print(f"MLP Mean Squared Error: {mlp_mse:.5f}")
print(f"MLP R-squared: {mlp_r2:.5f}")

json_report_data["mlp_results"] = {
    "mse": mlp_mse,
    "r2": mlp_r2,
    "predictions": mlp_preds.tolist()
}

# 3. Feature Importance (from GBR)
feature_importances = gb_model.feature_importances_
importance_df = pd.DataFrame({'Feature': poly_feature_names, 'Importance': feature_importances})
importance_df = importance_df.sort_values(by='Importance', ascending=False)
json_report_data["feature_importances"] = importance_df.to_dict(orient="records")

# Visualization: Feature Importance
plt.figure(figsize=(12, 8))
sns.barplot(x='Importance', y='Feature', data=importance_df.head(10))
plt.title('Top 10 Feature Importances (Gradient Boosting)')
plt.savefig("plot_reports/p4.1_feature_importances.png", dpi=150, bbox_inches="tight")
plt.show()

# Visualization: Model Comparison (Actual vs Predicted)
plt.figure(figsize=(12, 6))
plt.plot(df['Frame'], y, label='Actual Balance Index', color='blue', alpha=0.5)
plt.plot(df['Frame'], gb_preds, label='GBR Predictions', color='red', linestyle='--')
plt.plot(df['Frame'], mlp_preds, label='MLP Predictions', color='green', linestyle=':')
plt.title('Model Comparison: Actual vs Predicted Balance Index')
plt.xlabel('Frame')
plt.ylabel('Balance Index')
plt.legend()
plt.savefig("plot_reports/p4.1_model_comparison.png", dpi=150, bbox_inches="tight")
plt.show()

json_report_data["actual_vs_predicted"] = {
    "frame": df["Frame"].tolist(),
    "actual": y.tolist(),
    "gbr": gb_preds.tolist(),
    "mlp": mlp_preds.tolist()
}

# Save JSON Report
json_report_file = "json_reports/p4.1_gradient_boosting_equation_extraction.json"
with open(json_report_file, "w", encoding="utf-8") as f:
    json.dump(json_report_data, f, indent=2, ensure_ascii=False)

# Save results
df['GBR_Predictions'] = gb_preds
df['MLP_Predictions'] = mlp_preds
df.to_csv('csv/gradient_boosting_results.csv', index=False)
print("Analysis completed. Data saved to gradient_boosting_results.csv.")
print(f"JSON report saved to {json_report_file}")
