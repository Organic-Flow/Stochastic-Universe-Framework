import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from sklearn.cluster import KMeans
import seaborn as sns
import json

os.makedirs("csv", exist_ok=True)
os.makedirs("plot_reports", exist_ok=True)
os.makedirs("json_reports", exist_ok=True)

# Load the CSV file
file_path = 'csv/frame_analysis_results.csv'
data = pd.read_csv(file_path)

# JSON Report Data
json_report_data = {
    "phase": "Spectral and Cluster Analysis",
    "name": "Advanced Pattern Analysis",
    "correlation_matrix": data.corr().to_dict()
}

# 1. Fourier Transform for Quantum Coherence
def analyze_fourier(data, column, sample_rate=1):
    signal = data[column].values
    n = len(signal)
    yf = fft(signal)
    xf = fftfreq(n, 1 / sample_rate)[:n // 2]
    
    amplitude = 2.0 / n * np.abs(yf[:n // 2])

    plt.figure(figsize=(10, 6))
    plt.plot(xf, amplitude)
    plt.title(f"Fourier Transform of {column}")
    plt.xlabel("Frequency")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.savefig(f"plot_reports/fourier_transform_{column.lower().replace(' ', '_')}.png", dpi=150, bbox_inches="tight")
    plt.close()
    
    json_report_data["fourier_analysis"] = {
        "column": column,
        "frequency": xf.tolist(),
        "amplitude": amplitude.tolist()
    }

analyze_fourier(data, "Quantum Coherence")

# 2. Clustering (K-Means) for Avg Intensity and Quantum Coherence
def clustering_analysis(data, features, n_clusters=3):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_data = data[features].values
    kmeans.fit(cluster_data)
    data['Cluster'] = kmeans.labels_

    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        x=features[0],
        y=features[1],
        hue='Cluster',
        palette='viridis',
        data=data
    )
    plt.title(f"K-Means Clustering ({features[0]} vs {features[1]})")
    plt.xlabel(features[0])
    plt.ylabel(features[1])
    plt.grid()
    plt.savefig("plot_reports/kmeans_clustering.png", dpi=150, bbox_inches="tight")
    plt.close()
    
    json_report_data["clustering_analysis"] = {
        "features": features,
        "data": data[features + ['Cluster']].to_dict(orient="records")
    }

clustering_analysis(data, ["Avg Intensity", "Quantum Coherence"])

# 3. Heatmap of Correlations
def correlation_heatmap(data):
    plt.figure(figsize=(8, 6))
    correlation_matrix = data.corr()
    sns.heatmap(
        correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True
    )
    plt.title("Heatmap of Correlations")
    plt.savefig("plot_reports/correlation_heatmap.png", dpi=150, bbox_inches="tight")
    plt.close()

correlation_heatmap(data)

# 4. Combined Analysis of Avg Intensity and Quantum Coherence
plt.figure(figsize=(10, 6))
plt.plot(data["Frame"], data["Avg Intensity"], label="Avg Intensity", color="blue")
plt.plot(data["Frame"], data["Quantum Coherence"], label="Quantum Coherence", color="green")
plt.title("Combined Analysis: Avg Intensity vs Quantum Coherence")
plt.xlabel("Frame")
plt.ylabel("Values")
plt.legend()
plt.grid()
plt.savefig("plot_reports/combined_intensity_coherence.png", dpi=150, bbox_inches="tight")
plt.close()

json_report_data["combined_analysis"] = {
    "frame": data["Frame"].tolist(),
    "avg_intensity": data["Avg Intensity"].tolist(),
    "quantum_coherence": data["Quantum Coherence"].tolist()
}

# Save JSON Report
json_report_file = "json_reports/spectral_and_cluster_analysis.json"
with open(json_report_file, "w", encoding="utf-8") as f:
    json.dump(json_report_data, f, indent=2, ensure_ascii=False)

print(f"JSON report saved to {json_report_file}")
