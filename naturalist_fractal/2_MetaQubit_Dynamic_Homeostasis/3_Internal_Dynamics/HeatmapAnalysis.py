import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from meta_qubit import MetaQubit

PLOTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "analysis_plots")

class MetaQubitHeatmapAnalysis:
    def __init__(self, num_metaqubits, qubits_per_meta=4, noise_level=0.05):
        self.num_metaqubits = num_metaqubits
        self.qubits_per_meta = qubits_per_meta
        self.noise_level = noise_level
        self.meta_circuit = MetaQubit(num_qubits=qubits_per_meta)
        self.coherence_data = []
        self.entanglement_data = []
        self.noise_data = []

    def analyze(self, params):
        """Analysis of coherence, entanglement, and noise."""
        coherence = np.abs(np.sum(np.sin(params)))
        entanglement = np.sum(params ** 2)
        noise = np.mean(np.random.normal(0, self.noise_level, len(params)))
        self.coherence_data.append(coherence)
        self.entanglement_data.append(entanglement)
        self.noise_data.append(noise)

    def run_analysis(self):
        """Run analysis for different numbers of meta-qubits."""
        for i in range(1, self.num_metaqubits + 1):
            params = np.random.uniform(0, 2 * np.pi, i)
            self.analyze(params)

    def plot_heatmaps(self):
        """Create heatmaps for analysis visualization."""
        x = np.arange(1, self.num_metaqubits + 1)
        y = np.arange(1, self.num_metaqubits + 1)
        mesh_x, mesh_y = np.meshgrid(x, y)

        coherence_matrix = np.tile(self.coherence_data, (len(x), 1)).T
        entanglement_matrix = np.tile(self.entanglement_data, (len(x), 1)).T
        noise_matrix = np.tile(self.noise_data, (len(x), 1)).T

        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        ax1, ax2, ax3, ax4 = axes.flatten()

        # Coherence Heatmap
        c1 = ax1.pcolormesh(mesh_x, mesh_y, coherence_matrix, cmap='Blues', shading='auto')
        fig.colorbar(c1, ax=ax1)
        ax1.set_title("Coherence Heatmap")
        ax1.set_xlabel("MetaQubits")
        ax1.set_ylabel("MetaQubits")

        # Entanglement Heatmap
        c2 = ax2.pcolormesh(mesh_x, mesh_y, entanglement_matrix, cmap='Greens', shading='auto')
        fig.colorbar(c2, ax=ax2)
        ax2.set_title("Entanglement Heatmap")
        ax2.set_xlabel("MetaQubits")
        ax2.set_ylabel("MetaQubits")

        # Noise Heatmap
        c3 = ax3.pcolormesh(mesh_x, mesh_y, noise_matrix, cmap='Reds', shading='auto')
        fig.colorbar(c3, ax=ax3)
        ax3.set_title("Noise Heatmap")
        ax3.set_xlabel("MetaQubits")
        ax3.set_ylabel("MetaQubits")

        # Combined Map
        combined_matrix = coherence_matrix + entanglement_matrix - noise_matrix
        c4 = ax4.pcolormesh(mesh_x, mesh_y, combined_matrix, cmap='Purples', shading='auto')
        fig.colorbar(c4, ax=ax4)
        ax4.set_title("Combined Map")
        ax4.set_xlabel("MetaQubits")
        ax4.set_ylabel("MetaQubits")

        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, "heatmap_analysis.png"), dpi=150, bbox_inches='tight')
        plt.close()
        print(f"Saved: heatmap_analysis.png")


# Run analysis
if __name__ == "__main__":
    num_metaqubits = 6
    heatmap_analysis = MetaQubitHeatmapAnalysis(num_metaqubits)
    heatmap_analysis.run_analysis()
    heatmap_analysis.plot_heatmaps()
