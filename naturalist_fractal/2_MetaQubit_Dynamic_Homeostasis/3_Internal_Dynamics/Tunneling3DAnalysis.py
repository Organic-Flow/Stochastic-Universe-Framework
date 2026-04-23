import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import json
import sys

# Add the parent directory to sys.path to import meta_qubit
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
try:
    from naturalist_fractal.meta_qubit import MetaQubit
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from meta_qubit import MetaQubit

PLOTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "analysis_plots")
JSON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "json_reports")
os.makedirs(PLOTS_DIR, exist_ok=True)
os.makedirs(JSON_DIR, exist_ok=True)

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
            tunneling_scores.append(float(np.mean(np.sin(param_set))))
        return tunneling_scores

    def noise_analysis(self, params):
        """Add noise to the data."""
        return [float(v) for v in np.random.normal(0, self.noise_level, len(params))]

    def coherence_analysis(self, params):
        """Coherence analysis."""
        return [float(np.sum(np.cos(param_set))) for param_set in params]

    def entanglement_analysis(self, params):
        """Entanglement analysis."""
        return [float(np.prod(np.sin(param_set) ** 2)) for param_set in params]

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
        
        # Save to JSON
        json_report_data = {
            "name": "MetaQubit Tunneling and Correlation Analysis",
            "tunneling": tunneling,
            "coherence": coherence,
            "entanglement": entanglement,
            "noise": noise
        }
        json_report_file = os.path.join(JSON_DIR, "tunneling_3d_analysis.json")
        with open(json_report_file, "w", encoding="utf-8") as f:
            json.dump(json_report_data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved: tunneling_3d_analysis.png and {json_report_file}")

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
