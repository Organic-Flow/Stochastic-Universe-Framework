import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from mpl_toolkits.mplot3d import Axes3D

os.makedirs("csv", exist_ok=True)
os.makedirs("plot_reports", exist_ok=True)


# 1. Load data
df = pd.read_csv('csv/final_balance_analysis.csv')

# 2. Calculate new indices (if not already present)
if 'Balance Index' not in df.columns:
    df['Balance Index'] = df['Avg Intensity'] + df['Max Intensity'] / 2

# 3. Data exploration
print("Statistical Features:")
print(df.describe())
print("\nVariable Correlations:")
correlation_matrix = df[['Frame', 'Avg Intensity', 'Balance Index']].corr()
print(correlation_matrix)

# 4. Visualize distributions
plt.figure(figsize=(10, 6))
sns.kdeplot(df['Avg Intensity'], label="Avg Intensity", color="blue", fill=True)
sns.kdeplot(df['Balance Index'], label="Balance Index", color="green", fill=True)
plt.title("Distribution of Average Intensity and Balance Index")
plt.xlabel("Values")
plt.ylabel("Density")
plt.legend()
plt.savefig("plot_reports/p2.4_balance_index_distribution.png", dpi=150, bbox_inches="tight")
plt.show()

# 5. Analyze polynomial equation
X = df['Frame'].values.reshape(-1, 1)
y = df['Balance Index'].values

# Polynomial Terms
poly = PolynomialFeatures(degree=3)
X_poly = poly.fit_transform(X)

# Model training
model = LinearRegression()
model.fit(X_poly, y)
y_pred = model.predict(X_poly)

# Display equation
coefficients = model.coef_
intercept = model.intercept_
print("\nModel Coefficients:", coefficients)
print(f"Balance Equation:\nBalance Index = {intercept:.5f} + " +
      " + ".join([f"{coefficients[i]:.5f}*Frame^{i}" for i in range(1, len(coefficients))]))

# Model evaluation
mse = mean_squared_error(y, y_pred)
r2 = r2_score(y, y_pred)
print(f"Mean Squared Error (MSE): {mse:.5f}")
print(f"R-squared (R2): {r2:.5f}")

# 6. Visualize actual and predicted values
plt.figure(figsize=(10, 6))
plt.scatter(df['Frame'], df['Balance Index'], label="Actual", color="blue")
plt.plot(df['Frame'], y_pred, label="Predicted", color="red")
plt.title("Actual vs Predicted Average Intensity")
plt.xlabel("Frame")
plt.ylabel("Avg Intensity")
plt.legend()
plt.savefig("plot_reports/p2.4_polynomial_balance_fit.png", dpi=150, bbox_inches="tight")
plt.show()

# 7. 3D Visualization
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(df['Frame'], df['Avg Intensity'], df['Balance Index'],
                     c=df['Balance Index'], cmap='viridis')
ax.set_title("3D Visualization: Frame vs Avg Intensity vs Balance Index")
ax.set_xlabel("Frame")
ax.set_ylabel("Avg Intensity")
ax.set_zlabel("Balance Index")
fig.colorbar(scatter, ax=ax, label="Balance Index")
plt.savefig("plot_reports/p2.4_3d_balance_index.png", dpi=150, bbox_inches="tight")
plt.show()

# 8. Heatmap of correlations
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", cbar=True)
plt.title("Variable Correlations")
plt.savefig("plot_reports/p2.4_correlation_heatmap.png", dpi=150, bbox_inches="tight")
plt.show()

# 9. Save new data
df['Predicted Balance Index'] = y_pred
df.to_csv('csv/enhanced_balance_analysis.csv', index=False)
print("\nAnalysis completed. Data saved to enhanced_balance_analysis.csv.")
