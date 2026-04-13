import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from meta_qubit import MetaQubit  # Import MetaQubit

# Parameters for the fractal
grid_size = 100  # Reduction for 3D rendering
depth = 50  # Slightly reduced recursion depth
scale = 1.5
stochastic_factor = 0.003

# Range for three axes
x = np.linspace(-1.5, 1.5, grid_size)
y = np.linspace(-1.5, 1.5, grid_size)
X, Y = np.meshgrid(x, y)
Z = X + 1j * Y

# Simulated MetaQubit
try:
    meta_qubit = MetaQubit(num_qubits=8)
except ImportError:
    class SimulatedMetaQubit:
        """Simulate quantum output if real hardware is unavailable."""
        def run_circuit(self):
            return np.random.uniform(0.9, 1.1, size=(100,))
    meta_qubit = SimulatedMetaQubit()

# Quantum-enhanced fractal function for a 3D perspective
def quantum_fractal_3D(Z, depth, scale, stochastic_factor):
    """
    Generate a 3D Naturalist Fractal using recursion with stability enhancements.
    """
    if depth == 0:
        return np.exp(-np.abs(Z))  # Basic geometry

    # Quantum randomness
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

# Parameter adjustment
depth = 7  # Controlled recursion
scale = 1.2  # Reduced scale
stochastic_factor = 0.001  # Lower stochasticity


# Calculate fractal for grid
F_global = quantum_fractal_3D(Z, depth, scale, stochastic_factor)

# Normalize for 3D visualization
F_global_normalized = F_global / np.max(F_global)

# Three-dimensional visualization
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Visualization using height (z) as fractal intensity
ax.plot_surface(
    X, Y, F_global_normalized.real,  # Use the real part
    cmap='viridis', edgecolor='none'
)

# Add axis details
ax.set_title('3D Naturalist Fractal')
ax.set_xlabel('Longitude-like dimension (Re)')
ax.set_ylabel('Latitude-like dimension (Im)')
ax.set_zlabel('Fractal Intensity')
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fractal_frames", "naturalist_fractal_3D.png")
plt.savefig(output_path, dpi=150, bbox_inches='tight')
plt.close()
print(f"Saved: {output_path}")
