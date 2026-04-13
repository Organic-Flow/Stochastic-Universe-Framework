import os
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

os.makedirs("csv", exist_ok=True)
os.makedirs("plot_reports", exist_ok=True)


# 1. Load and prepare data
data = pd.read_csv('csv/enhanced_balance_analysis.csv')  # Replace with your file
features = ['Frame', 'Avg Intensity', 'Max Intensity', 'Predicted Max Intensity']  # Adapt based on your data
target = 'Balance Index'

# Clean data
data = data.dropna()
X = data[features]
y = data[target]

# Split data into training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. Develop Gradient Boosting Regressor
model = GradientBoostingRegressor(n_estimators=500, learning_rate=0.01, max_depth=4, random_state=42)
model.fit(X_train, y_train)

# 3. Predictions and evaluation
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

train_mse = mean_squared_error(y_train, y_pred_train)
test_mse = mean_squared_error(y_test, y_pred_test)
train_r2 = r2_score(y_train, y_pred_train)
test_r2 = r2_score(y_test, y_pred_test)

print(f"Train MSE: {train_mse}")
print(f"Test MSE: {test_mse}")
print(f"Train R²: {train_r2}")
print(f"Test R²: {test_r2}")

# 4. Feature importance
feature_importance = model.feature_importances_
sorted_idx = np.argsort(feature_importance)
plt.barh(np.array(features)[sorted_idx], feature_importance[sorted_idx], color='blue')
plt.xlabel("Importance")
plt.title("Feature Importance (Gradient Boosting)")
plt.savefig("plot_reports/p4.2_feature_importances.png", dpi=150, bbox_inches="tight")
plt.show()

# 5. Simplified equation based on importance
important_features = np.array(features)[sorted_idx][-3:]  # The 3 most important features
print(f"Important Features: {important_features}")

# 6. Final equation based on important features
simplified_model = GradientBoostingRegressor(n_estimators=500, learning_rate=0.01, max_depth=3, random_state=42)
simplified_model.fit(X_train[important_features], y_train)

y_pred_simplified = simplified_model.predict(X_test[important_features])
simplified_mse = mean_squared_error(y_test, y_pred_simplified)
simplified_r2 = r2_score(y_test, y_pred_simplified)

print(f"Simplified Equation - MSE: {simplified_mse}")
print(f"Simplified Equation - R²: {simplified_r2}")

# 7. Graph of actual and predicted values
plt.plot(y_test.values, label="Actual Balance Index", color='blue')
plt.plot(y_pred_simplified, label="Predicted Balance Index", color='orange', linestyle='--')
plt.legend()
plt.xlabel("Samples")
plt.ylabel("Balance Index")
plt.title("Actual vs Predicted Balance Index")
plt.savefig("plot_reports/p4.2_simplified_predictions.png", dpi=150, bbox_inches="tight")
plt.show()

# Save equation
coefficients = simplified_model.feature_importances_
print("Final Equation:")
for feature, coef in zip(important_features, coefficients):
    print(f"{coef:.6f} * {feature}")
