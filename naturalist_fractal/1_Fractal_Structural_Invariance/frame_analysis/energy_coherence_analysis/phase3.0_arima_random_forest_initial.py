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
df = pd.read_csv('csv/enhanced_balance_analysis.csv')

# JSON Report Data
json_report_data = {
    "phase": "3.0",
    "name": "ARIMA and Random Forest Initial",
    "correlation_matrix": df[['Frame', 'Avg Intensity', 'Balance Index']].corr().to_dict()
}

# 1. Correlation Matrix Heatmap
plt.figure(figsize=(10, 8))
correlation_matrix = df[['Frame', 'Avg Intensity', 'Balance Index']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Variable Correlations')
plt.savefig("plot_reports/p3.0_correlation_heatmap.png", dpi=150, bbox_inches="tight")
plt.show()

# 2. ARIMA Model (Time Series)
def run_arima(df):
    model = ARIMA(df['Balance Index'], order=(1, 1, 1))
    results = model.fit()
    df['ARIMA_Fit'] = results.fittedvalues
    
    plt.figure(figsize=(12, 6))
    plt.plot(df['Frame'], df['Balance Index'], label='Actual Balance Index', color='blue')
    plt.plot(df['Frame'], df['ARIMA_Fit'], label='ARIMA Fit', color='red', linestyle='--')
    plt.title('ARIMA Time-Series Fit: Balance Index')
    plt.xlabel('Frame')
    plt.ylabel('Balance Index')
    plt.legend()
    plt.savefig("plot_reports/p3.0_arima_timelapse.png", dpi=150, bbox_inches="tight")
    plt.show()
    json_report_data["arima_fit"] = df[["Frame", "Balance Index", "ARIMA_Fit"]].to_dict(orient="records")

run_arima(df)

# 3. Random Forest (Predictive Modeling)
def run_random_forest(df):
    X = df[['Frame', 'Avg Intensity']]
    y = df['Balance Index']
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    df['RF_Predictions'] = model.predict(X)
    
    mse = mean_squared_error(y, df['RF_Predictions'])
    r2 = r2_score(y, df['RF_Predictions'])
    print(f"RF Mean Squared Error: {mse:.5f}")
    print(f"RF R-squared: {r2:.5f}")
    
    plt.figure(figsize=(12, 6))
    plt.scatter(df['Frame'], y, label='Actual Balance Index', color='blue', alpha=0.6)
    plt.plot(df['Frame'], df['RF_Predictions'], label='RF Predictions', color='green', linewidth=2)
    plt.title('Random Forest Predictions: Balance Index')
    plt.xlabel('Frame')
    plt.ylabel('Balance Index')
    plt.legend()
    plt.savefig("plot_reports/p3.0_rf_predictions.png", dpi=150, bbox_inches="tight")
    plt.show()
    
    json_report_data["rf_predictions"] = {
        "data": df[["Frame", "Balance Index", "RF_Predictions"]].to_dict(orient="records"),
        "mse": mse,
        "r2": r2,
        "feature_importances": dict(zip(X.columns, model.feature_importances_.tolist()))
    }

run_random_forest(df)

# Save JSON Report
json_report_file = "json_reports/p3.0_arima_random_forest_initial.json"
with open(json_report_file, "w", encoding="utf-8") as f:
    json.dump(json_report_data, f, indent=2, ensure_ascii=False)

# Save results
df.to_csv('csv/arima_rf_initial_results.csv', index=False)
print("Analysis completed. Data saved to arima_rf_initial_results.csv.")
print(f"JSON report saved to {json_report_file}")
