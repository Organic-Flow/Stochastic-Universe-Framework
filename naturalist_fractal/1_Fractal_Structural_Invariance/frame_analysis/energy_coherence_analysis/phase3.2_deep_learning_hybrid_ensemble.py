import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.decomposition import PCA
from sklearn.metrics import mean_squared_error, r2_score
from statsmodels.tsa.arima.model import ARIMA
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import matplotlib.pyplot as plt
import json

os.makedirs("csv", exist_ok=True)
os.makedirs("plot_reports", exist_ok=True)
os.makedirs("json_reports", exist_ok=True)

# 1. Load and prepare data
data = pd.read_csv("csv/enhanced_balance_analysis.csv")
numeric_cols = data.select_dtypes(include=np.number).columns
data = data[numeric_cols].dropna()

# Create new features
data['Rate_of_Change'] = data['Avg Intensity'].diff().fillna(0)
data['Intensity_Ratio'] = data['Avg Intensity'] / data['Balance Index']

# 2. PCA for dimensionality reduction
pca = PCA(n_components=2)
principal_components = pca.fit_transform(data[['Avg Intensity', 'Rate_of_Change', 'Intensity_Ratio']])
data['PCA1'], data['PCA2'] = principal_components[:, 0], principal_components[:, 1]

# 3. Calculate feature importance (Random Forest)
X_features = data[['Frame', 'Avg Intensity', 'Rate_of_Change', 'Intensity_Ratio', 'PCA1', 'PCA2']]
y_target = data['Balance Index']
rf_model = RandomForestRegressor(random_state=42)
rf_model.fit(X_features, y_target)
importances = rf_model.feature_importances_

# JSON Report Data
json_report_data = {
    "phase": "3.2",
    "name": "Deep Learning Hybrid Ensemble",
    "feature_importances": dict(zip(X_features.columns, importances.tolist()))
}

# 4. ARIMA for time series
arima_model = ARIMA(data['Balance Index'], order=(1, 1, 1)).fit()
arima_predictions = arima_model.predict(start=0, end=len(data)-1)

# 5. LSTM for prediction
time_steps = 10
X_lstm, y_lstm = [], []
for i in range(len(data) - time_steps):
    X_lstm.append(data[['Avg Intensity', 'Rate_of_Change', 'Intensity_Ratio']].iloc[i:i+time_steps].values)
    y_lstm.append(data['Balance Index'].iloc[i+time_steps])

X_lstm, y_lstm = np.array(X_lstm), np.array(y_lstm)
lstm_model = Sequential([
    LSTM(50, activation='relu', input_shape=(time_steps, X_lstm.shape[2])),
    Dense(1)
])
lstm_model.compile(optimizer='adam', loss='mse')
lstm_model.fit(X_lstm, y_lstm, epochs=50, batch_size=32, verbose=0)
lstm_predictions = lstm_model.predict(X_lstm)

# 6. Hybrid model (ARIMA + Random Forest)
data['ARIMA_Prediction'] = arima_predictions.values
data['Hybrid_Input'] = (data['ARIMA_Prediction'] + rf_model.predict(X_features)) / 2

# Final prediction
final_model = RandomForestRegressor(random_state=42)
final_model.fit(data[['Hybrid_Input', 'Avg Intensity', 'Rate_of_Change']], data['Balance Index'])
final_predictions = final_model.predict(data[['Hybrid_Input', 'Avg Intensity', 'Rate_of_Change']])

# 7. Evaluate results
mse = mean_squared_error(data['Balance Index'], final_predictions)
r2 = r2_score(data['Balance Index'], final_predictions)

json_report_data["hybrid_results"] = {
    "mse": mse,
    "r2": r2,
    "frame": data["Frame"].tolist(),
    "actual": data["Balance Index"].tolist(),
    "predicted": final_predictions.tolist()
}

# 8. Visualization
plt.figure(figsize=(10, 6))
plt.plot(data['Frame'], data['Balance Index'], label="Actual Balance Index")
plt.plot(data['Frame'], final_predictions, label="Final Predictions", linestyle="--")
plt.scatter([data['Frame'].iloc[np.argmax(final_predictions)]],
            [np.max(final_predictions)], color='green', label="Optimal Point")
plt.title("Optimal Balance Index (Hybrid Ensemble)")
plt.xlabel("Frame")
plt.ylabel("Balance Index")
plt.legend()
plt.savefig("plot_reports/p3.2_hybrid_predictions.png", dpi=150, bbox_inches="tight")
plt.show()

plt.figure(figsize=(10, 6))
plt.bar(X_features.columns, importances)
plt.title("Feature Importance (Random Forest - Hybrid)")
plt.xlabel("Features")
plt.ylabel("Importance")
plt.savefig("plot_reports/p3.2_feature_importances.png", dpi=150, bbox_inches="tight")
plt.show()

# 9. Extract equation
print("Final Equation:")
print(f"Balance Index = {importances[0]:.5f}*Frame + {importances[1]:.5f}*Avg Intensity + "
      f"{importances[2]:.5f}*Rate_of_Change + {importances[3]:.5f}*Intensity_Ratio")

# Save JSON Report
json_report_file = "json_reports/p3.2_deep_learning_hybrid_ensemble.json"
with open(json_report_file, "w", encoding="utf-8") as f:
    json.dump(json_report_data, f, indent=2, ensure_ascii=False)
print(f"JSON report saved to {json_report_file}")
