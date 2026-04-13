import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
from meta_qubit import MetaQubit

PLOTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "analysis_plots")

class Tunneling3DAnalysis:
    def __init__(self, num_metaqubits=6, qubits_per_meta=4, noise_level=0.05):
        self.num_metaqubits = num_metaqubits
        self.qubits_per_meta = qubits_per_meta
        self.noise_level = noise_level
        self.meta_circuit = MetaQubit(num_qubits=self.qubits_per_meta)

    def tunneling_analysis(self, params):
        """Tunneling measurements."""
        tunneling_scores = []
        for param_set in params:
            tunneling_scores.append(np.mean(np.sin(param_set)))  # Example tunneling measurement
        return tunneling_scores

    def noise_analysis(self, params):
        """Add noise to the data."""
        return np.random.normal(0, self.noise_level, len(params))

    def coherence_analysis(self, params):
        """Coherence analysis."""
        return [np.sum(np.cos(param_set)) for param_set in params]

    def entanglement_analysis(self, params):
        """Entanglement analysis."""
        return [np.prod(np.sin(param_set) ** 2) for param_set in params]

    def generate_3d_plot(self, tunneling, coherence, entanglement, noise):
        """Create 3D scatter plot for correlation."""
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        # Scatter plot for tunneling, coherence, entanglement
        scatter = ax.scatter(tunneling, coherence, entanglement, c=noise, cmap='viridis', s=50)
        ax.set_xlabel('Tunneling')
        ax.set_ylabel('Coherence')
        ax.set_zlabel('Entanglement')
        ax.set_title('3D Analysis of Correlations')

        # Add color bar for noise
        cbar = plt.colorbar(scatter, ax=ax, pad=0.1)
        cbar.set_label('Noise Level')

        plt.savefig(os.path.join(PLOTS_DIR, "tunneling_3d_analysis.png"), dpi=150, bbox_inches='tight')
        plt.close()
        print(f"Saved: tunneling_3d_analysis.png")

    def run_analysis(self):
        """Run analysis."""
        # Create parameters for analysis
        params = [np.random.uniform(0, 2 * np.pi, self.qubits_per_meta) for _ in range(self.num_metaqubits)]

        tunneling = self.tunneling_analysis(params)
        coherence = self.coherence_analysis(params)
        entanglement = self.entanglement_analysis(params)
        noise = self.noise_analysis(params)

        # Create 3D plot
        self.generate_3d_plot(tunneling, coherence, entanglement, noise)

# Run analysis
if __name__ == "__main__":
    analysis = Tunneling3DAnalysis(num_metaqubits=6, qubits_per_meta=16, noise_level=0.1)
    analysis.run_analysis()
