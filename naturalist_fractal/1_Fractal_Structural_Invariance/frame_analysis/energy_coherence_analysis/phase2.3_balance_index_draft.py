import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score

# Load data from the CSV file
df = pd.read_csv("csv/enhanced_analysis_with_predictions.csv")

# Statistical features
print("Statistical features:")
print(df.describe())

# Create new balance index
df["Balance Index"] = df["Avg Intensity"] * (1 / (1 + df["Avg Intensity"].var()))

# Visualize distribution of Average Intensity and Balance Index
plt.figure(figsize=(10, 6))
sns.kdeplot(df["Avg Intensity"], label="Avg Intensity", color="blue", fill=True, alpha=0.5)
sns.kdeplot(df["Balance Index"], label="Balance Index", color="green", fill=True, alpha=0.5)
plt.title("Distribution of Average Intensity and Balance Index")
plt.xlabel("Values")
plt.ylabel("Density")
plt.legend()
plt.savefig("plot_reports/p2.3_balance_index_distribution.png", dpi=150, bbox_inches="tight")
plt.show()

# Correlation analysis
correlation_matrix = df[["Frame", "Avg Intensity", "Balance Index"]].corr()
print("Variable correlations:")
print(correlation_matrix)

# Visualize correlations
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Variable Correlations")
plt.savefig("plot_reports/p2.3_correlation_heatmap.png", dpi=150, bbox_inches="tight")
plt.show()

# Polynomial regression to predict Average Intensity
X = df["Frame"].values.reshape(-1, 1)
y = df["Avg Intensity"].values

# Polynomial transformation
poly = PolynomialFeatures(degree=3)
X_poly = poly.fit_transform(X)

# Model training
model = LinearRegression()
model.fit(X_poly, y)

# Prediction and evaluation
y_pred = model.predict(X_poly)
mse = mean_squared_error(y, y_pred)
r2 = r2_score(y, y_pred)
print(f"Mean Squared Error (MSE): {mse:.5f}")
print(f"R-squared (R2): {r2:.5f}")

# Model coefficients
print("Model coefficients:", model.coef_)

# Visualize prediction vs actual values
plt.figure(figsize=(10, 6))
plt.scatter(df["Frame"], y, label="Actual", color="blue", alpha=0.6)
plt.plot(df["Frame"], y_pred, label="Predicted", color="red", linewidth=2)
plt.title("Actual vs Predicted Average Intensity")
plt.xlabel("Frame")
plt.ylabel("Avg Intensity")
plt.legend()
plt.savefig("plot_reports/p2.3_polynomial_avg_intensity.png", dpi=150, bbox_inches="tight")
plt.show()

# 3D Visualization: Frame vs Avg Intensity vs Balance Index
from mpl_toolkits.mplot3d import Axes3D

os.makedirs("csv", exist_ok=True)
os.makedirs("plot_reports", exist_ok=True)


fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection="3d")
scatter = ax.scatter(df["Frame"], df["Avg Intensity"], df["Balance Index"], c=df["Balance Index"], cmap="viridis")
ax.set_title("3D Visualization: Frame vs Avg Intensity vs Balance Index")
ax.set_xlabel("Frame")
ax.set_ylabel("Avg Intensity")
ax.set_zlabel("Balance Index")
fig.colorbar(scatter, ax=ax, label="Balance Index")
plt.savefig("plot_reports/p2.3_3d_balance_index.png", dpi=150, bbox_inches="tight")
plt.show()

# Balance Equation
coefficients = model.coef_
intercept = model.intercept_
print("Balance Equation:")
print(f"Balance Index = {coefficients[0]:.5f} + {coefficients[1]:.5f}*Frame + {coefficients[2]:.5f}*Frame^2 + {coefficients[3]:.5f}*Frame^3 + {intercept:.5f}")

# Save results
df["Predicted Balance Index"] = y_pred
df.to_csv("csv/final_balance_analysis.csv", index=False)
print("Analysis completed. Data saved to final_balance_analysis.csv.")
