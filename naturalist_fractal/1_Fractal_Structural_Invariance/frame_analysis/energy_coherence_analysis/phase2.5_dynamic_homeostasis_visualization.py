import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

os.makedirs("csv", exist_ok=True)
os.makedirs("plot_reports", exist_ok=True)


# 1. Load data
df = pd.read_csv('csv/enhanced_balance_analysis.csv')

# 2. Heatmap for Variable Correlations
def plot_correlation_heatmap(df):
    plt.figure(figsize=(8, 6))
    correlation_matrix = df[['Frame', 'Avg Intensity', 'Balance Index']].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Variable Correlations')
    plt.savefig("plot_reports/p2.5_correlation_heatmap.png", dpi=150, bbox_inches="tight")
    plt.show()

plot_correlation_heatmap(df)

# 3. 3D Visualization (Frame vs Avg Intensity vs Balance Index)
def plot_3d_visualization(df):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(df['Frame'], df['Avg Intensity'], df['Balance Index'],
                         c=df['Balance Index'], cmap='viridis', s=50)
    ax.set_xlabel('Frame')
    ax.set_ylabel('Avg Intensity')
    ax.set_zlabel('Balance Index')
    plt.title('3D Visualization: Frame vs Avg Intensity vs Balance Index')
    fig.colorbar(scatter, label='Balance Index')
    plt.savefig("plot_reports/p2.5_3d_balance_index.png", dpi=150, bbox_inches="tight")
    plt.show()

plot_3d_visualization(df)

# 4. Time-Lapse Visualization (Balance Index per Frame)
def create_time_lapse(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(df['Frame'].min(), df['Frame'].max())
    ax.set_ylim(df['Balance Index'].min(), df['Balance Index'].max())
    ax.set_xlabel('Frame')
    ax.set_ylabel('Balance Index')
    ax.set_title('Time-Lapse of Balance Index per Frame')
    line, = ax.plot([], [], lw=2)

    def update(frame):
        data = df[df['Frame'] <= frame]
        line.set_data(data['Frame'], data['Balance Index'])
        return line,

    ani = FuncAnimation(fig, update, frames=df['Frame'], blit=True, interval=100)
    plt.show()

create_time_lapse(df)

# 5. Balance Optimization (Gradient Descent)
def balance_optimization(df):
    # Define the balance function
    def balance_function(frame):
        return 0.41698 + 0.00426 * frame - 0.00001 * frame**2 + 0.00000 * frame**3

    df['Optimized Balance'] = balance_function(df['Frame'])
    plt.figure(figsize=(10, 6))
    plt.plot(df['Frame'], df['Balance Index'], label='Actual Balance Index', color='blue')
    plt.plot(df['Frame'], df['Optimized Balance'], label='Optimized Balance', color='red', linestyle='--')
    plt.xlabel('Frame')
    plt.ylabel('Balance Index')
    plt.title('Balance Optimization')
    plt.legend()
    plt.savefig("plot_reports/p2.5_balance_optimization.png", dpi=150, bbox_inches="tight")
    plt.show()

balance_optimization(df)

# 6. Heatmap for Balance Index per Frame and Average Intensity
def balance_index_heatmap(df):
    heatmap_data = df.pivot_table(index='Frame', values='Balance Index', aggfunc='mean')
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, cmap='YlGnBu', annot=False)
    plt.title('Heatmap: Balance Index per Frame')
    plt.xlabel('Frame')
    plt.ylabel('Balance Index')
    plt.savefig("plot_reports/p2.5_balance_index_heatmap.png", dpi=150, bbox_inches="tight")
    plt.show()

balance_index_heatmap(df)
