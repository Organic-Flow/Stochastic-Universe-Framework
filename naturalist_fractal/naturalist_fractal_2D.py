import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from meta_qubit import MetaQubit  # Import MetaQubit

# Parameters for the fractal
grid_size = 2000  # High resolution
depth = 30  # Increased recursion depth
scale = 1.5  # Enhanced scale
stochastic_factor = 0.003  # Controlled stochastic noise

# Focus on a small region of the fractal
x = np.linspace(-0.5, 0.5, grid_size)  # Limited region
y = np.linspace(-0.5, 0.5, grid_size)
X, Y = np.meshgrid(x, y)
Z = X + 1j * Y  # Complex plane

# MetaQubit simulation
try:
    meta_qubit = MetaQubit(num_qubits=10)  # Using MetaQubit
except ImportError:
    class SimulatedMetaQubit:
        """Simulate quantum output if real hardware is unavailable."""
        def run_circuit(self):
            return np.random.uniform(0.9, 1.1, size=(100,))

    meta_qubit = SimulatedMetaQubit()

# Quantum-enhanced fractal function for a local region
def localized_quantum_fractal(Z, depth, scale, stochastic_factor):
    """
    Generate a localized view of the Naturalist Fractal.
    """
    if depth == 0:
        return np.exp(-np.abs(Z))  # Basic fractal structure

    # Quantum processing or simulation
    quantum_output = meta_qubit.run_circuit()
    quantum_factor = np.mean(quantum_output)

    # Limit numerical overflow
    Z = np.clip(Z, -1e3, 1e3)
    Z_abs = np.clip(np.abs(Z), 0, 50)

    # Calculate fractal evolution
    Z_new = (
        Z**2 +
        scale * np.sin(Z_abs**2) * quantum_factor +
        stochastic_factor * np.cos(2 * np.angle(Z))
    )

    return localized_quantum_fractal(Z_new, depth - 1, scale / 1.2, stochastic_factor / 1.2) + np.exp(-Z_abs)

# Generate the localized fractal
F_global = localized_quantum_fractal(Z, depth, scale, stochastic_factor)

# Normalize for visualization
F_global_normalized = F_global / np.max(F_global)

# Visualize the localized fractal with a richer palette
plt.figure(figsize=(12, 12))
plt.imshow(F_global_normalized, extent=[-0.5, 0.5, -0.5, 0.5], cmap='inferno')  # Use rich palette
plt.colorbar(label='Fractal Intensity')
plt.title('Localized Naturalist Fractal with Enhanced Color Palette')
plt.xlabel('Longitude-like dimension (Re)')
plt.ylabel('Latitude-like dimension (Im)')
plt.savefig("naturalist_fractal_2D.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved: naturalist_fractal_2D.png")
