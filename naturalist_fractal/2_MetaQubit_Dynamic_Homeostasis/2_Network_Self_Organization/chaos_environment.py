import os
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import json
import sys

# Add parent directory for MetaQubit import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
try:
    from naturalist_fractal.meta_qubit import MetaQubit
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    try:
        from meta_qubit import MetaQubit
    except ImportError:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
        from meta_qubit import MetaQubit

# matplotlib parameters
plt.rcParams.update({
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "legend.fontsize": 10,
    "figure.titlesize": 16
})

os.makedirs("images", exist_ok=True)
os.makedirs("json_reports", exist_ok=True)

def create_dynamic_network(num_nodes):
    network = nx.complete_graph(num_nodes)
    for u, v in network.edges:
        network[u][v]['weight'] = np.random.uniform(-1, 1)
    return network

def update_network(network, meta_qubit):
    output = meta_qubit.run_circuit()
    output_np = np.array(output)
    cost = -np.mean(output_np)
    
    # Use as many outputs as available, cycle if needed
    edges = list(network.edges)
    for i, (u, v) in enumerate(edges):
        network[u][v]['weight'] += float(output_np[i % len(output_np)])
    return network, cost

def run_multiple_simulations(meta_qubit, steps=100, nodes=10, repetitions=5):
    """Reduced parameters for stable execution in CI/CLI environment"""
    all_weights = np.zeros((repetitions, steps, nodes, nodes))
    all_costs = np.zeros((repetitions, steps))

    for r in range(repetitions):
        network = create_dynamic_network(nodes)
        for step in range(steps):
            network, cost = update_network(network, meta_qubit)
            all_costs[r, step] = cost
            for u, v in network.edges:
                all_weights[r, step, u, v] = network[u][v]['weight']
        if (r + 1) % 1 == 0:
            print(f"Completed repetition {r+1}/{repetitions}")
    return all_weights, all_costs

def analyze_results(all_weights):
    mean_weights = np.mean(all_weights, axis=0)
    std_weights = np.std(all_weights, axis=0)
    return mean_weights, std_weights

def analyze_costs(all_costs):
    mean_costs = np.mean(all_costs, axis=0)
    std_costs = np.std(all_costs, axis=0)
    return mean_costs, std_costs

def plot_convergence_of_weights(std_weights, steps):
    avg_std = np.mean(std_weights, axis=(1, 2))
    plt.figure(figsize=(10, 6))
    plt.plot(range(steps), avg_std, marker='o', linestyle='-', label='Mean STD of Weights')
    plt.xlabel("Simulation Steps")
    plt.ylabel("Standard Deviation")
    plt.title("Convergence of Edge Weights Variance")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("images/convergence_weights.png", dpi=150)
    plt.close()
    return avg_std.tolist()

def plot_cost_convergence(mean_costs, std_costs, steps):
    x = np.arange(steps)
    plt.figure(figsize=(10, 6))
    plt.plot(x, mean_costs, color='blue', label='Mean Cost')
    plt.fill_between(x, mean_costs - std_costs, mean_costs + std_costs,
                     color='blue', alpha=0.2, label='Std Dev')
    plt.xlabel("Simulation Steps")
    plt.ylabel("Cost")
    plt.title("Cost Convergence Over Simulation Steps")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("images/convergence_cost.png", dpi=150)
    plt.close()
    return mean_costs.tolist(), std_costs.tolist()

def plot_weight_histograms(all_weights, step_indices):
    n_nodes = all_weights.shape[2]
    histogram_data = {}
    for step in step_indices:
        weights_list = []
        for r in range(all_weights.shape[0]):
            for u in range(n_nodes):
                for v in range(u + 1, n_nodes):
                    weights_list.append(float(all_weights[r, step, u, v]))
        
        plt.figure(figsize=(10, 6))
        plt.hist(weights_list, bins=30, alpha=0.8, color='green', edgecolor='black')
        plt.xlabel("Edge Weight")
        plt.ylabel("Frequency")
        plt.title(f"Histogram of Edge Weights at Step {step}")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"images/histogram_weights_step_{step}.png", dpi=150)
        plt.close()
        histogram_data[str(step)] = weights_list
    return histogram_data

if __name__ == "__main__":
    plt.switch_backend('Agg')
    meta_qubit = MetaQubit(num_qubits=8)

    # Managed parameters for reliable output
    STEPS = 50
    NODES = 10
    REPETITIONS = 5

    print(f"Starting Network Self-Organization simulation ({STEPS} steps)...")
    all_weights, all_costs = run_multiple_simulations(meta_qubit, steps=STEPS, nodes=NODES, repetitions=REPETITIONS)

    mean_weights, std_weights = analyze_results(all_weights)
    mean_costs, std_costs = analyze_costs(all_costs)

    avg_std_list = plot_convergence_of_weights(std_weights, STEPS)
    mean_costs_list, std_costs_list = plot_cost_convergence(mean_costs, std_costs, STEPS)
    hist_data = plot_weight_histograms(all_weights, [0, STEPS // 2, STEPS - 1])

    # Save to JSON
    json_report_data = {
        "name": "Network Self-Organization Analysis",
        "steps": STEPS,
        "nodes": NODES,
        "repetitions": REPETITIONS,
        "weight_variance_convergence": avg_std_list,
        "cost_convergence": {
            "mean": mean_costs_list,
            "std": std_costs_list
        },
        "weight_histograms": hist_data
    }
    
    json_report_file = "json_reports/network_self_organization.json"
    with open(json_report_file, "w", encoding="utf-8") as f:
        json.dump(json_report_data, f, indent=2, ensure_ascii=False)
    
    print(f"Analysis completed. Images saved in images/ and JSON report in {json_report_file}")
