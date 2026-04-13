import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.decomposition import PCA
from statsmodels.tsa.arima.model import ARIMA

# Step 1: Load data
data = pd.read_csv('csv/enhanced_balance_analysis.csv')

# Create new features (Feature Engineering)
data['Rate_of_Change'] = data['Avg Intensity'].diff().fillna(0)  # Rate of change
data['Intensity_Ratio'] = data['Avg Intensity'] / data['Max Intensity']  # Ratio

# Step 2: Visualize correlation heatmap
# Filter only numeric columns
numeric_data = data.select_dtypes(include=[np.number])

# Check if the DataFrame contains only numbers
print("Numeric Columns in DataFrame:")
print(numeric_data.head())

# Calculate correlations
correlation_matrix = numeric_data.corr()

# Visualize Heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title("Heatmap: Variable Correlations")
plt.savefig("plot_reports/p3.0_correlation_heatmap.png", dpi=150, bbox_inches="tight")
plt.show()


# Step 3: PCA for dimensionality reduction
pca = PCA(n_components=2)
pca_features = pca.fit_transform(data[['Avg Intensity', 'Rate_of_Change', 'Intensity_Ratio']])
data['PCA1'] = pca_features[:, 0]
data['PCA2'] = pca_features[:, 1]

# Step 4: Prepare data for non-linear models
X = data[['Frame', 'Avg Intensity', 'Rate_of_Change', 'PCA1', 'PCA2']]
y = data['Balance Index']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest Regressor
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Predictions
y_pred = rf_model.predict(X_test)

# Evaluate performance
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse:.5f}")
print(f"R-squared: {r2:.5f}")

# Step 5: Visualize model results
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, color='blue', alpha=0.6, label='Predictions')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', lw=2, label='Ideal Fit')
plt.xlabel("Actual Balance Index")
plt.ylabel("Predicted Balance Index")
plt.title("Actual vs Predicted Balance Index")
plt.legend()
plt.savefig("plot_reports/p3.0_rf_predictions.png", dpi=150, bbox_inches="tight")
plt.show()

# Step 6: Time-Series Analysis
# Trend analysis with ARIMA
model_arima = ARIMA(data['Balance Index'], order=(1, 1, 1))
arima_result = model_arima.fit()
print(arima_result.summary())

# Step 7: Visualize time-lapse
plt.figure(figsize=(10, 6))
plt.plot(data['Frame'], data['Balance Index'], label='Actual Balance Index')
plt.plot(data['Frame'], arima_result.fittedvalues, label='ARIMA Fit', color='red')
plt.title("Time-Lapse: Balance Index")
plt.xlabel("Frame")
plt.ylabel("Balance Index")
plt.legend()
plt.savefig("plot_reports/p3.0_arima_timelapse.png", dpi=150, bbox_inches="tight")
plt.show()

# Step 8: Dynamic optimization
from scipy.optimize import minimize

os.makedirs("csv", exist_ok=True)
os.makedirs("plot_reports", exist_ok=True)


# Objective: Maximum balance
def objective_function(params):
    frame, avg_intensity = params
    return -rf_model.predict([[frame, avg_intensity, 0, 0, 0]])[0]  # Negative for maximum value

# Initial constraints (customize as needed)
bounds = [(data['Frame'].min(), data['Frame'].max()),
          (data['Avg Intensity'].min(), data['Avg Intensity'].max())]

result = minimize(objective_function, x0=[300, 0.7], bounds=bounds)
optimal_frame, optimal_intensity = result.x
print(f"Optimal Frame: {optimal_frame}")
print(f"Optimal Avg Intensity: {optimal_intensity}")

# Step 9: Final visualization of optimal points
plt.figure(figsize=(10, 6))
plt.plot(data['Frame'], data['Balance Index'], label='Actual Balance Index')
plt.scatter(optimal_frame, rf_model.predict([[optimal_frame, optimal_intensity, 0, 0, 0]])[0],
            color='green', label='Optimal Point', s=100)
plt.title("Optimal Balance Index")
plt.xlabel("Frame")
plt.ylabel("Balance Index")
plt.legend()
plt.savefig("plot_reports/p3.0_optimal_balance.png", dpi=150, bbox_inches="tight")
plt.show()
