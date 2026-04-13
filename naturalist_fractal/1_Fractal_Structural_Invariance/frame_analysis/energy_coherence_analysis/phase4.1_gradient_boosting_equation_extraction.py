import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

os.makedirs("csv", exist_ok=True)
os.makedirs("plot_reports", exist_ok=True)


# Load Data
file_path = "csv/enhanced_balance_analysis.csv"  # Update with your file
data = pd.read_csv(file_path)

# Data Preprocessing
data = data.dropna()  # Remove empty rows
numeric_columns = data.select_dtypes(include=[np.number]).columns
data = data[numeric_columns]  # Use only numeric columns

# Data Normalization
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data)
scaled_data = pd.DataFrame(scaled_data, columns=numeric_columns)

# Features and Target
X = scaled_data.drop("Balance Index", axis=1)
y = scaled_data["Balance Index"]

# Split Data into Training and Testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Non-Linear Analysis (Polynomial Features)
poly = PolynomialFeatures(degree=3, include_bias=False)
X_poly_train = poly.fit_transform(X_train)
X_poly_test = poly.transform(X_test)

# Gradient Boosting Model
gbr = GradientBoostingRegressor(n_estimators=200, learning_rate=0.1, max_depth=3, random_state=42)
gbr.fit(X_poly_train, y_train)

# Prediction and Evaluation - Gradient Boosting
y_pred_gbr = gbr.predict(X_poly_test)
mse_gbr = mean_squared_error(y_test, y_pred_gbr)
r2_gbr = r2_score(y_test, y_pred_gbr)

print("Gradient Boosting - MSE:", mse_gbr)
print("Gradient Boosting - R^2:", r2_gbr)

# Neural Network Model
nn = MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42)
nn.fit(X_train, y_train)

# Prediction and Evaluation - Neural Network
y_pred_nn = nn.predict(X_test)
mse_nn = mean_squared_error(y_test, y_pred_nn)
r2_nn = r2_score(y_test, y_pred_nn)

print("Neural Network - MSE:", mse_nn)
print("Neural Network - R^2:", r2_nn)

# Extract Coefficients - Gradient Boosting
feature_importances = gbr.feature_importances_
poly_features = poly.get_feature_names_out(X.columns)

# Visualize Feature Importance
plt.figure(figsize=(10, 6))
plt.barh(poly_features, feature_importances)
plt.title("Feature Importance (Gradient Boosting)")
plt.xlabel("Importance")
plt.ylabel("Features")
plt.savefig("plot_reports/p4.1_feature_importances.png", dpi=150, bbox_inches="tight")
plt.show()

# Extract Final Equation
final_coefficients = feature_importances * scaler.scale_[-1]
print("Final Equation (Gradient Boosting):")
for i, coeff in enumerate(final_coefficients):
    print(f"{coeff:.6f} * {poly_features[i]}")

# Visualize Results
plt.figure(figsize=(10, 6))
plt.plot(y_test.reset_index(drop=True), label="Actual Balance Index", color="blue")
plt.plot(y_pred_gbr, label="Gradient Boosting Predictions", color="orange", linestyle="--")
plt.plot(y_pred_nn, label="Neural Network Predictions", color="green", linestyle=":")
plt.legend()
plt.title("Actual vs Predicted Results")
plt.xlabel("Samples")
plt.ylabel("Balance Index")
plt.savefig("plot_reports/p4.1_model_comparison.png", dpi=150, bbox_inches="tight")
plt.show()
