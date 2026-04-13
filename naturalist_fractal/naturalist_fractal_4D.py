import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from meta_qubit import MetaQubit  # Import MetaQubit

# Parameters for the fractal
grid_size = 100
max_depth = 30  # Maximum recursion depth
scale = 1.5
stochastic_factor = 0.003

# Range for three axes
x = np.linspace(-1.5, 1.5, grid_size)
y = np.linspace(-1.5, 1.5, grid_size)
X, Y = np.meshgrid(x, y)
Z = X + 1j * Y

# MetaQubit integration
try:
    meta_qubit = MetaQubit(num_qubits=8)  # Using MetaQubit
except ImportError:
    class SimulatedMetaQubit:
        """Simulate quantum output if real hardware is unavailable."""
        def run_circuit(self):
            return np.random.uniform(0.9, 1.1, size=(100,))
    meta_qubit = SimulatedMetaQubit()

# Quantum-enhanced fractal function for a 3D perspective
def quantum_fractal_3D(Z, depth, scale, stochastic_factor):
    """
    Generate a 3D Naturalist Fractal using recursion with MetaQubit integration.
    """
    if depth == 0:
        return np.exp(-np.abs(Z))  # Basic geometry

    # Using MetaQubit
    quantum_output = meta_qubit.run_circuit()
    quantum_factor = np.mean(quantum_output)

    # Calculate new geometry with value constraints
    Z_new = (
        Z**2 +
        scale * np.sin(np.abs(Z)**2) * quantum_factor +
        stochastic_factor * np.cos(2 * np.angle(Z))
    )
    Z_new = np.clip(Z_new, -1e2, 1e2)  # Value constraints

    return quantum_fractal_3D(Z_new, depth - 1, scale / 1.2, stochastic_factor / 1.2) + np.exp(-np.abs(Z))

# Animation function
def update(frame):
    global ax
    ax.clear()
    depth = frame + 1  # Increase depth at each frame
    F = quantum_fractal_3D(Z, depth, scale, stochastic_factor)
    F_normalized = F / np.max(F)
    ax.plot_surface(
        X, Y, F_normalized.real,  # Use the real part
        cmap='viridis', edgecolor='none'
    )
    ax.set_title(f'4D Naturalist Fractal - Depth {depth}')
    ax.set_xlabel('Longitude-like dimension (Re)')
    ax.set_ylabel('Latitude-like dimension (Im)')
    ax.set_zlabel('Fractal Intensity')

# Setup figure for animation
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Create animation
anim = FuncAnimation(
    fig, update, frames=max_depth, interval=500, repeat=True
)

# Save animation as MP4
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fractal_frames", "naturalist_fractal_4D.gif")
writer = PillowWriter(fps=2)
anim.save(output_path, writer=writer)
plt.close()
print(f"Saved: {output_path}")
