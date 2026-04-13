import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from meta_qubit import MetaQubit

# matplotlib parameters for a more professional appearance
plt.rcParams.update({
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "legend.fontsize": 10,
    "figure.titlesize": 16
})


def create_dynamic_network(num_nodes):
    """
    Creates a dynamic network as a complete graph with random initial weights.

    Parameters:
        num_nodes (int): Number of nodes in the graph.

    Returns:
        network (networkx.Graph): Complete graph with stochastic edge weights.
    """
    network = nx.complete_graph(num_nodes)
    for u, v in network.edges:
        network[u][v]['weight'] = np.random.uniform(-1, 1)
    return network


def update_network(network, meta_qubit):
    """
    Updates the network based on the output of the MetaQubit.

    The MetaQubit's circuit output is used to update the weight of each edge.
    A simple cost function is defined as the negative mean of the output.

    Parameters:
        network (networkx.Graph): The current network graph.
        meta_qubit (MetaQubit): Instance of the MetaQubit class.

    Returns:
        network (networkx.Graph): Updated network.
        cost (float): Cost value computed as -mean(output).
    """
    output = meta_qubit.run_circuit()
    output_np = output.detach().numpy() if hasattr(output, "detach") else np.array(output)
    cost = -np.mean(output_np)
    for (u, v), w in zip(network.edges, output_np):
        network[u][v]['weight'] += float(w)
    return network, cost


def run_multiple_simulations(meta_qubit, steps=300, nodes=100, repetitions=50):
    """
    Runs multiple simulations of the network update process.

    For each repetition, a dynamic network is created and updated over a number of steps.
    The function records the evolution of edge weights and the cost function at each step.

    Parameters:
        meta_qubit (MetaQubit): Instance of the MetaQubit class.
        steps (int): Number of simulation steps.
        nodes (int): Number of nodes in the network.
        repetitions (int): Number of repetitions (independent runs).

    Returns:
        all_weights (ndarray): Array of shape (repetitions, steps, nodes, nodes) containing edge weights.
        all_costs (ndarray): Array of shape (repetitions, steps) containing the cost at each step.
    """
    all_weights = np.zeros((repetitions, steps, nodes, nodes))
    all_costs = np.zeros((repetitions, steps))

    for r in range(repetitions):
        network = create_dynamic_network(nodes)
        for step in range(steps):
            network, cost = update_network(network, meta_qubit)
            all_costs[r, step] = cost
            for u, v in network.edges:
                all_weights[r, step, u, v] = network[u][v]['weight']
    return all_weights, all_costs


def analyze_results(all_weights):
    """
    Analyzes the simulation results by calculating the mean and standard deviation of edge weights.

    Parameters:
        all_weights (ndarray): Array containing the edge weights over the simulation.

    Returns:
        mean_weights (ndarray): Mean weights per step.
        std_weights (ndarray): Standard deviation of weights per step.
    """
    mean_weights = np.mean(all_weights, axis=0)
    std_weights = np.std(all_weights, axis=0)
    return mean_weights, std_weights


def analyze_costs(all_costs):
    """
    Analyzes the cost evolution by computing the mean and standard deviation across repetitions.

    Parameters:
        all_costs (ndarray): Array containing cost values over simulation steps.

    Returns:
        mean_costs (ndarray): Mean cost per step.
        std_costs (ndarray): Standard deviation of cost per step.
    """
    mean_costs = np.mean(all_costs, axis=0)
    std_costs = np.std(all_costs, axis=0)
    return mean_costs, std_costs


def plot_convergence_of_weights(std_weights, steps):
    """
    Plots the convergence of the network based on the standard deviation of edge weights over time.

    Parameters:
        std_weights (ndarray): Standard deviation of weights at each simulation step.
        steps (int): Total number of simulation steps.
    """
    avg_std = np.mean(std_weights, axis=(1, 2))  # Average standard deviation across all edges per step

    plt.figure(figsize=(10, 6))
    plt.plot(range(steps), avg_std, marker='o', linestyle='-', label='Mean STD of Weights')
    plt.xlabel("Simulation Steps")
    plt.ylabel("Standard Deviation")
    plt.title("Convergence of Edge Weights Variance")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("convergence_weights.png", dpi=300)
    plt.show()


def plot_cost_convergence(mean_costs, std_costs, steps):
    """
    Plots the convergence of the cost function over simulation steps with error bars.

    Parameters:
        mean_costs (ndarray): Mean cost per step.
        std_costs (ndarray): Standard deviation of cost per step.
        steps (int): Total number of simulation steps.
    """
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
    plt.savefig("convergence_cost.png", dpi=300)
    plt.show()


def plot_weight_histograms(all_weights, step_indices):
    """
    Creates histograms of the edge weights for selected simulation steps.

    Only considers edges with u < v to avoid double-counting in the complete graph.

    Parameters:
        all_weights (ndarray): Array containing edge weights from the simulations.
        step_indices (list of int): Specific simulation steps to visualize.
    """
    n_nodes = all_weights.shape[2]
    for step in step_indices:
        weights_list = []
        for r in range(all_weights.shape[0]):
            for u in range(n_nodes):
                for v in range(u + 1, n_nodes):
                    weights_list.append(all_weights[r, step, u, v])
        weights_array = np.array(weights_list)

        plt.figure(figsize=(10, 6))
        plt.hist(weights_array, bins=30, alpha=0.8, color='green', edgecolor='black')
        plt.xlabel("Edge Weight")
        plt.ylabel("Frequency")
        plt.title(f"Histogram of Edge Weights at Step {step}")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"histogram_weights_step_{step}.png", dpi=300)
        plt.show()


# --------------------- Main Program --------------------- #
if __name__ == "__main__":
    # Initialize MetaQubit instance with 12 qubits
    meta_qubit = MetaQubit(num_qubits=12)

    # Simulation parameters
    STEPS = 300 # Up to 1000
    NODES = 100
    REPETITIONS = 50

    # Run multiple simulations to record edge weights and cost values
    all_weights, all_costs = run_multiple_simulations(meta_qubit, steps=STEPS, nodes=NODES, repetitions=REPETITIONS)

    # Analyze the simulation results
    mean_weights, std_weights = analyze_results(all_weights)
    mean_costs, std_costs = analyze_costs(all_costs)

    # Plot convergence of edge weights variance
    plot_convergence_of_weights(std_weights, STEPS)

    # Plot cost convergence over simulation steps
    plot_cost_convergence(mean_costs, std_costs, STEPS)

    # Plot histograms for selected steps (e.g., initial, middle, final)
    plot_weight_histograms(all_weights, [0, STEPS // 2, STEPS - 1])
