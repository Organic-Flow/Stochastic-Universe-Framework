import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from sklearn.cluster import KMeans
import seaborn as sns

os.makedirs("csv", exist_ok=True)
os.makedirs("plot_reports", exist_ok=True)

# Load the CSV file
file_path = 'csv/frame_analysis_results.csv'
data = pd.read_csv(file_path)

# Basic analysis
print("First lines of the file:")
print(data.head())
print("\nStatistics:")
print(data.describe())

# 1. Fourier Transform for Quantum Coherence
def analyze_fourier(data, column, sample_rate=1):
    signal = data[column].values
    n = len(signal)
    yf = fft(signal)
    xf = fftfreq(n, 1 / sample_rate)[:n // 2]

    plt.figure(figsize=(10, 6))
    plt.plot(xf, 2.0 / n * np.abs(yf[:n // 2]))
    plt.title(f"Fourier Transform of {column}")
    plt.xlabel("Frequency")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.savefig(f"plot_reports/fourier_transform_{column.lower().replace(' ', '_')}.png", dpi=150, bbox_inches="tight")
    plt.show()

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
    plt.show()

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
    plt.show()

correlation_heatmap(data)

# 4. Animated Graph for Avg Intensity and Quantum Coherence
import matplotlib.animation as animation

def animate_analysis(data, x_column, y_column):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, len(data))
    ax.set_ylim(data[y_column].min(), data[y_column].max())
    line, = ax.plot([], [], lw=2)

    def update(frame):
        line.set_data(data[x_column][:frame], data[y_column][:frame])
        return line,

    ani = animation.FuncAnimation(fig, update, frames=len(data), interval=50, blit=True)
    plt.title(f"Animation of {y_column} Over Frames")
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.show()

animate_analysis(data, "Frame", "Avg Intensity")

# 5. Combined Analysis of Avg Intensity and Quantum Coherence
plt.figure(figsize=(10, 6))
plt.plot(data["Frame"], data["Avg Intensity"], label="Avg Intensity", color="blue")
plt.plot(data["Frame"], data["Quantum Coherence"], label="Quantum Coherence", color="green")
plt.title("Combined Analysis: Avg Intensity vs Quantum Coherence")
plt.xlabel("Frame")
plt.ylabel("Values")
plt.legend()
plt.grid()
plt.savefig("plot_reports/combined_intensity_coherence.png", dpi=150, bbox_inches="tight")
plt.show()
