import os
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import json
import sys

# Add the parent directory to sys.path to import meta_qubit
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
try:
    from naturalist_fractal.meta_qubit import MetaQubit
except ImportError:
    # Fallback for local execution
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    try:
        from meta_qubit import MetaQubit
    except ImportError:
        # Final fallback
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
        from meta_qubit import MetaQubit

os.makedirs("analysis_plots", exist_ok=True)
os.makedirs("visualize", exist_ok=True)
os.makedirs("json_reports", exist_ok=True)

# Calculate entropy
def calculate_entropy(values):
    probabilities = (values - min(values)) / (max(values) - min(values) + 1e-9)
    probabilities = probabilities / np.sum(probabilities)
    return -np.sum(probabilities * np.log2(probabilities + 1e-9))

# Calculate coherence
def calculate_coherence(connections):
    if not connections: return 0
    return np.mean([weight for _, _, weight in connections])

# Calculate tunneling probability
def calculate_tunneling_probability(weight):
    return np.exp(-weight)  # Exponential decrease of probability with weight

# Create graph
def create_advanced_graph(meta_qubit, num_frames):
    num_qubits = meta_qubit.num_qubits
    frames_data = []
    
    # Store global stats for JSON
    global_stats = {
        "num_qubits": num_qubits,
        "num_frames": num_frames,
        "evolution": []
    }

    for f in range(num_frames):
        output = meta_qubit.run_circuit()
        G = nx.Graph()
        
        frame_nodes = []
        for i in range(num_qubits):
            state = '|1>' if output[i] > 0 else '|0>'
            G.add_node(i, state=state, value=float(output[i]))
            frame_nodes.append({
                "id": i,
                "state": state,
                "value": float(output[i])
            })

        weights = []
        tunnelings = []
        frame_edges = []
        for i in range(num_qubits):
            for j in range(i + 1, num_qubits):
                weight = np.abs(output[i] - output[j])
                tunneling = calculate_tunneling_probability(weight)
                G.add_edge(i, j, weight=float(weight), tunneling=float(tunneling))
                weights.append(weight)
                tunnelings.append(tunneling)
                if tunneling > 0.7: # Only store significant edges for JSON to keep it small
                    frame_edges.append({
                        "source": i,
                        "target": j,
                        "weight": float(weight),
                        "tunneling": float(tunneling)
                    })

        # Calculate measures for the frame
        entropy = calculate_entropy(output)
        coherence = calculate_coherence(G.edges(data='weight'))
        mean_weight = np.mean(weights)
        mean_tunneling = np.mean(tunnelings)

        global_stats["evolution"].append({
            "frame": f + 1,
            "entropy": float(entropy),
            "coherence": float(coherence),
            "mean_weight": float(mean_weight),
            "mean_tunneling": float(mean_tunneling),
            "nodes": frame_nodes,
            "edges": frame_edges
        })
        
        frames_data.append({
            "graph": G,
            "stats": global_stats["evolution"][-1]
        })
        
        if (f + 1) % 10 == 0:
            print(f"Generated frame {f + 1}/{num_frames}")

    return frames_data, global_stats

# Animation with tunneling indicators and detailed statistics
def animate_and_save(frames_data, global_stats, filename="visualize/meta_qubit_simulation.mp4"):
    fig, ax = plt.subplots(1, 2, figsize=(16, 8))
    pos = nx.circular_layout(frames_data[0]["graph"])

    def update(frame_idx):
        ax[0].clear()
        ax[1].clear()

        frame = frames_data[frame_idx]
        G = frame["graph"]
        stats = frame["stats"]
        evolution = global_stats["evolution"][:frame_idx+1]
        frames_range = range(1, frame_idx + 2)

        # Node colors based on state
        node_colors = ['red' if G.nodes[node]['state'] == '|1>' else 'blue' for node in G.nodes]
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=800, alpha=0.8, ax=ax[0])

        # Edges with dynamic thickness
        edges = G.edges(data=True)
        edge_weights = [edge[2]['weight'] for edge in edges]
        nx.draw_networkx_edges(G, pos, width=[2 * w for w in edge_weights], alpha=0.6, ax=ax[0])

        # Tunneling indicators with dots
        for u, v, d in G.edges(data=True):
            tunneling_prob = d['tunneling']
            if tunneling_prob > 0.7:
                mid_point = (pos[u] + pos[v]) / 2
                ax[0].scatter(*mid_point, s=tunneling_prob * 200, color='green', alpha=0.7)

        # Node labels
        labels = {node: f"Q{node}\n{G.nodes[node]['state']}\n({G.nodes[node]['value']:.2f})" for node in G.nodes}
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=10, ax=ax[0])

        # Title and settings
        ax[0].set_title(f"Frame {frame_idx+1}/{len(frames_data)} | Entropy: {stats['entropy']:.2f}, "
                        f"Coherence: {stats['coherence']:.2f}")
        ax[0].axis('off')

        # Statistics in the 2nd subplot
        ax[1].plot(frames_range, [e['entropy'] for e in evolution], label='Entropy', color='blue')
        ax[1].plot(frames_range, [e['coherence'] for e in evolution], label='Coherence', color='purple', linewidth=2)
        ax[1].plot(frames_range, [e['mean_weight'] for e in evolution], label='Mean Weight', color='orange')
        ax[1].plot(frames_range, [e['mean_tunneling'] for e in evolution], label='Mean Tunneling', color='green')
        
        ax[1].legend(loc='upper right')
        ax[1].set_xlabel('Frame')
        ax[1].set_ylabel('Value')
        ax[1].set_title("Evolution of Metrics Over Time")
        ax[1].grid(True)

    num_frames = len(frames_data)
    ani = FuncAnimation(fig, update, frames=num_frames, interval=500, repeat=False)
    
    # Save JSON Report
    json_report_file = "json_reports/meta_qubit_internal_dynamics.json"
    with open(json_report_file, "w", encoding="utf-8") as f:
        json.dump(global_stats, f, indent=2, ensure_ascii=False)
    print(f"JSON report saved to {json_report_file}")

    # Save Animation
    try:
        import matplotlib.animation as animation
        # Try MP4 first, fallback to GIF if ffmpeg is missing
        if os.system("ffmpeg -version > /dev/null 2>&1") == 0:
            writer = animation.FFMpegWriter(fps=2, metadata={"title": "MetaQubit Simulation"})
            ani.save(filename, writer=writer)
            print(f"🎥 Simulation saved as {filename}")
        else:
            gif_filename = filename.replace(".mp4", ".gif")
            ani.save(gif_filename, writer='pillow', fps=2)
            print(f"🎥 Simulation saved as {gif_filename} (FFMpeg not found)")
    except Exception as e:
        print(f"Error saving animation: {e}")
    
    plt.close()

if __name__ == "__main__":
    meta_qubit = MetaQubit(num_qubits=8)
    num_frames = 50
    print(f"Starting MetaQubit internal dynamics simulation ({num_frames} frames)...")
    frames_data, global_stats = create_advanced_graph(meta_qubit, num_frames)
    
    # Use Agg backend for headless execution
    plt.switch_backend('Agg')
    animate_and_save(frames_data, global_stats)
