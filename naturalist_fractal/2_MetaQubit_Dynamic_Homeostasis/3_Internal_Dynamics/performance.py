import numpy as np
import pennylane as qml
import time
import scipy.stats
import scipy.fftpack
import scipy.spatial
from scipy.linalg import svd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import json
import sys
from sklearn.decomposition import PCA
from sklearn.metrics import mutual_info_score

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

# --- Create Quality Information Generator --- #
def generate_quality_data(size=1024, method="chaotic"):
    """Generates quality information for MetaQubit"""
    if method == "chaotic":
        x = np.zeros(size)
        x[0] = 0.5
        r = 3.99
        for i in range(1, size):
            x[i] = r * x[i - 1] * (1 - x[i - 1])
        return x
    elif method == "fractal":
        return np.cumsum(np.random.randn(size))
    elif method == "stochastic":
        return np.sin(np.linspace(0, 50, size)) + np.random.normal(0, 0.1, size)
    else:
        raise ValueError("Unknown data generation method")

# --- Initialize MetaQubit --- #
metaqubit = MetaQubit(num_qubits=8)

def multi_qubit_circuit():
    """Quantum circuit with 8 qubits for comparison with MetaQubit."""
    dev = qml.device("default.qubit", wires=8)
    @qml.qnode(dev)
    def circuit():
        for i in range(8):
            qml.Hadamard(wires=i)
        return [qml.expval(qml.PauliZ(i)) for i in range(8)]
    return np.array(circuit())

# --- Calculate Information Capacity --- #
def compute_information_capacity(output):
    """Calculates information capacity based on entropy and complexity."""
    hist, _ = np.histogram(output, bins=50)
    entropy_output = scipy.stats.entropy(hist)
    variance = np.var(output)
    kolmogorov_complexity = np.log2(len(output)) / (variance + 1e-10)
    return float(entropy_output * kolmogorov_complexity)

# --- Test on MetaQubit and 8-Qubit System --- #
def test_qubits(data):
    start_time_meta = time.time()
    output_meta = metaqubit.run_circuit()
    end_time_meta = time.time()

    start_time_qubit = time.time()
    # For performance comparison, we simulate the standard system for the same data size
    output_qubit = np.array([multi_qubit_circuit() for _ in range(10)]) # Sample 10 times
    end_time_qubit = time.time()

    capacity_meta = compute_information_capacity(output_meta)
    capacity_qubit = compute_information_capacity(output_qubit.mean(axis=1))

    return {
        "metaqubit": {
            "output": [float(v) for v in output_meta],
            "time": end_time_meta - start_time_meta,
            "capacity": capacity_meta
        },
        "qubit": {
            "output": [float(v) for v in output_qubit.mean(axis=1)],
            "time": end_time_qubit - start_time_qubit,
            "capacity": capacity_qubit
        }
    }

# --- Experiment and Report Generation --- #
global_report = {
    "name": "MetaQubit vs Standard Qubit System Performance",
    "methods": {}
}

for method in ["chaotic", "fractal", "stochastic"]:
    print(f"Analyzing performance: {method}...")
    data = generate_quality_data(size=128, method=method) # Smaller size for visualization report
    results = test_qubits(data)
    
    # Visualization
    plt.figure(figsize=(12, 5))
    plt.plot(data, label='Input', alpha=0.7)
    plt.plot(results['metaqubit']['output'], label='MetaQubit', alpha=0.7)
    plt.plot(results['qubit']['output'], label='Standard 8-Qubit', linestyle='dashed')
    plt.legend()
    plt.title(f'Performance Comparison: {method.capitalize()} Input')
    plt.savefig(os.path.join(PLOTS_DIR, f"performance_{method}.png"), dpi=150, bbox_inches='tight')
    plt.close()

    global_report["methods"][method] = {
        "input": [float(v) for v in data],
        "metaqubit_output": results['metaqubit']['output'],
        "qubit_output": results['qubit']['output'],
        "metaqubit_capacity": results['metaqubit']['capacity'],
        "qubit_capacity": results['qubit']['capacity'],
        "metaqubit_time": results['metaqubit']['time'],
        "qubit_time": results['qubit']['time']
    }

# Save JSON Report
json_report_file = os.path.join(JSON_DIR, "performance_comparison.json")
with open(json_report_file, "w", encoding="utf-8") as f:
    json.dump(global_report, f, indent=2, ensure_ascii=False)

print(f"Analysis completed. JSON report saved to {json_report_file}")
