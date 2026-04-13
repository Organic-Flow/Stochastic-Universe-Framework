import numpy as np
import pennylane as qml
from meta_qubit import MetaQubit
import time
import scipy.stats
import scipy.fftpack
import scipy.spatial
from scipy.linalg import svd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from sklearn.decomposition import PCA
from sklearn.metrics import mutual_info_score

PLOTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "analysis_plots")


# --- Create Quality Information Generator --- #
def generate_quality_data(size=1024, method="chaotic"):
    """
    Generates quality information for MetaQubit
    """
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


# --- Initialize Qubit and MetaQubit --- #
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
    entropy_output = scipy.stats.entropy(np.histogram(output, bins=50)[0])
    kolmogorov_complexity = np.log2(len(output)) / np.var(output)
    return entropy_output * kolmogorov_complexity


# --- Test on MetaQubit and 8-Qubit System --- #
def test_qubits(data):
    start_time_meta = time.time()
    output_meta = metaqubit.run_circuit()
    end_time_meta = time.time()

    start_time_qubit = time.time()
    output_qubit = np.array([multi_qubit_circuit() for _ in range(len(data))])
    end_time_qubit = time.time()

    capacity_meta = compute_information_capacity(output_meta)
    capacity_qubit = compute_information_capacity(output_qubit.mean(axis=1))

    return {
        "metaqubit": {
            "output": output_meta,
            "time": end_time_meta - start_time_meta,
            "capacity": capacity_meta
        },
        "qubit": {
            "output": output_qubit.mean(axis=1),  # Mean value from 8 qubits
            "time": end_time_qubit - start_time_qubit,
            "capacity": capacity_qubit
        }
    }


# --- Run Experiment for different inputs --- #
for method in ["chaotic", "fractal", "stochastic"]:
    print(f"\n--- Testing for input method: {method} ---")
    data = generate_quality_data(size=1024, method=method)
    results = test_qubits(data)

    print(f"MetaQubit execution time: {results['metaqubit']['time']:.5f} sec")
    print(f"8-Qubit System execution time: {results['qubit']['time']:.5f} sec")

    correlation_meta = np.corrcoef(data[:len(results['metaqubit']['output'])], results['metaqubit']['output'])[0, 1]
    correlation_qubit = np.corrcoef(data[:len(results['qubit']['output'])], results['qubit']['output'])[0, 1]

    print(f"Input-Output Correlation (MetaQubit): {correlation_meta:.5f}")
    print(f"Input-Output Correlation (8-Qubit System): {correlation_qubit:.5f}")
    print(f"Information Capacity (MetaQubit): {results['metaqubit']['capacity']:.5f}")
    print(f"Information Capacity (8-Qubit System): {results['qubit']['capacity']:.5f}")


# --- Visualization of Results --- #
def plot_results(data, output_meta, output_qubit, method):
    plt.figure(figsize=(12, 5))
    plt.plot(data, label='Input', alpha=0.7)
    plt.plot(output_meta, label='MetaQubit', alpha=0.7)
    plt.plot(output_qubit, label='8-Qubit System', linestyle='dashed')
    plt.legend()
    plt.title(f'Input-Output Comparison for {method} Input')
    plt.savefig(os.path.join(PLOTS_DIR, f"performance_{method}.png"), dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: performance_{method}.png")


for method in ["chaotic", "fractal", "stochastic"]:
    data = generate_quality_data(size=1024, method=method)
    results = test_qubits(data)
    plot_results(data, results['metaqubit']['output'], results['qubit']['output'], method)