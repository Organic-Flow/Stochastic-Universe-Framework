import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
from meta_qubit import MetaQubit  # Import MetaQubit

# Create folder for saving frames
output_folder = "frames4"
raw_output_folder = "raw_frames4"  # Raw grayscale PNGs for CV2 geometric analysis
os.makedirs(output_folder, exist_ok=True)
os.makedirs(raw_output_folder, exist_ok=True)

# Parameters for the fractal
grid_size = 2000  # High resolution
depth = 30  # Increased recursion depth
scale = 1.5  # Enhanced scale

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

# Parameters for animation
initial_stochastic_factor = 0.803  # New initial value
frames = 200

# Loop for generating and saving frames
for frame in range(801, 801 + frames):  # Start from frame 101
    stochastic_factor = initial_stochastic_factor + (frame - 801) * 0.001  # Increase stochastic factor
    print(f"Generating frame {frame} with stochastic factor {stochastic_factor:.3f}")

    # Generate fractal for current stochastic factor
    F_frame = localized_quantum_fractal(Z, depth, scale, stochastic_factor)
    F_frame_normalized = F_frame / np.max(F_frame)

    # Plot and save the frame
    plt.figure(figsize=(12, 12))
    plt.imshow(F_frame_normalized.real, extent=[-0.5, 0.5, -0.5, 0.5], cmap='inferno')
    plt.colorbar(label='Fractal Intensity')
    plt.title(f'Frame {frame} | Stochastic Factor: {stochastic_factor:.3f}')
    plt.xlabel('Longitude-like dimension (Re)')
    plt.ylabel('Latitude-like dimension (Im)')

    # Save the matplotlib figure frame (for visualization)
    output_path = os.path.join(output_folder, f"frame_{frame:03d}.png")
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    # Save raw grayscale array (for CV2 geometric analysis — no matplotlib framing)
    raw_array = (F_frame_normalized.real * 255).astype(np.uint8)
    raw_path = os.path.join(raw_output_folder, f"frame_{frame:03d}.png")
    cv2.imwrite(raw_path, raw_array)

print(f"Frames saved in folder: {output_folder}")
print(f"Raw grayscale frames saved in folder: {raw_output_folder}")
