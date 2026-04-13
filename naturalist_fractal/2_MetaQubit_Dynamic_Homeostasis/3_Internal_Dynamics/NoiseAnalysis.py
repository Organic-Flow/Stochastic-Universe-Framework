import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pennylane as qml
import os
from meta_qubit import MetaQubit

PLOTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "analysis_plots")

class NoiseAnalysis:
    def __init__(self, num_metaqubits=6, qubits_per_meta=16, noise_levels=None):
        if noise_levels is None:
            noise_levels = [0.0, 0.05, 0.1, 0.15, 0.2]
        self.num_metaqubits = num_metaqubits
        self.qubits_per_meta = qubits_per_meta
        self.noise_levels = noise_levels
        self.meta_circuit = MetaQubit(num_qubits=self.qubits_per_meta)

    def tunneling_analysis(self, noise_level):
        """Analyze tunneling with noise."""
        noisy_params = self.meta_circuit.params + np.random.normal(0, noise_level, len(self.meta_circuit.params))
        results = self.meta_circuit.qnode(noisy_params)
        return np.mean(results)

    def coherence_analysis(self, noise_level):
        """Analyze coherence with noise."""
        noisy_params = self.meta_circuit.params + np.random.normal(0, noise_level, len(self.meta_circuit.params))
        state = self.meta_circuit.qnode(noisy_params)
        coherence = np.linalg.norm(state)  # Coherence is the norm of the state vector
        return coherence

    def entanglement_analysis(self, noise_level):
        """Analyze entanglement with noise."""
        noisy_params = self.meta_circuit.params + np.random.normal(0, noise_level, len(self.meta_circuit.params))
        results = self.meta_circuit.qnode(noisy_params)
        mutual_information = -np.sum(np.log2(np.abs(results) + 1e-10))  # Approximation for analysis
        return mutual_information

    def generate_analysis(self):
        """Generate data10 for tunneling, coherence, and entanglement analysis."""
        tunneling_data, coherence_data, entanglement_data = [], [], []

        for noise_level in self.noise_levels:
            tunneling = self.tunneling_analysis(noise_level)
            coherence = self.coherence_analysis(noise_level)
            entanglement = self.entanglement_analysis(noise_level)

            tunneling_data.append(tunneling)
            coherence_data.append(coherence)
            entanglement_data.append(entanglement)

        return tunneling_data, coherence_data, entanglement_data

    def plot_3d_analysis(self, tunneling_data, coherence_data, entanglement_data):
        """Plot a 3D analysis of the data10."""
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')

        sc = ax.scatter(
            tunneling_data,
            coherence_data,
            entanglement_data,
            c=self.noise_levels,
            cmap='viridis',
            s=100
        )

        ax.set_xlabel("Tunneling")
        ax.set_ylabel("Coherence")
        ax.set_zlabel("Entanglement")
        ax.set_title("3D Analysis of Noise Impact")
        plt.colorbar(sc, label="Noise Level")
        plt.savefig(os.path.join(PLOTS_DIR, "noise_3d_analysis.png"), dpi=150, bbox_inches='tight')
        plt.close()
        print(f"Saved: noise_3d_analysis.png")


# Experiment Execution
num_metaqubits = 6
qubits_per_meta = 16
noise_levels = [0.0, 0.05, 0.1, 0.15, 0.2]

analysis = NoiseAnalysis(num_metaqubits=num_metaqubits, qubits_per_meta=qubits_per_meta, noise_levels=noise_levels)
tunneling_data, coherence_data, entanglement_data = analysis.generate_analysis()
analysis.plot_3d_analysis(tunneling_data, coherence_data, entanglement_data)
