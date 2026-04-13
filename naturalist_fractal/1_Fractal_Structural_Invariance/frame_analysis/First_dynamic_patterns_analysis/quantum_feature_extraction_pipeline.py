import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from meta_qubit import MetaQubit  # Import MetaQubit

# Output directories
os.makedirs("csv", exist_ok=True)
os.makedirs("plot_reports", exist_ok=True)

# Locate frame folders
folders = ["frames", "frames1", "frames2", "frames3", "frames4"]

# Frame analysis class
class FrameAnalysis:
    def __init__(self, folders):
        self.folders = folders
        self.images = []

    def load_images(self):
        """Load all images from the folders."""
        for folder in self.folders:
            for file in sorted(os.listdir(folder)):
                if file.endswith(".png"):
                    img_path = os.path.join(folder, file)
                    img = np.array(Image.open(img_path).convert("L")) / 255.0  # Normalization
                    self.images.append(img)

    def analyze_images(self):
        """Analyze frames using MetaQubit."""
        # Create MetaQubit for analysis
        meta_qubit = MetaQubit(num_qubits=10)

        # Analyze each image
        results = []
        for idx, img in enumerate(self.images):
            avg_intensity = np.mean(img)
            max_intensity = np.max(img)

            # Run MetaQubit circuit
            quantum_result = meta_qubit.run_circuit()
            coherence_score = np.sum(quantum_result) / len(quantum_result)

            results.append({
                "Frame": idx + 1,
                "Avg Intensity": avg_intensity,
                "Max Intensity": max_intensity,
                "Quantum Coherence": coherence_score
            })

            if idx % 10 == 0:  # Update every 10 frames
                print(f"Analyzing Frame {idx + 1}/{len(self.images)}")

        return results

    def save_results(self, results, output_file="csv/frame_analysis_results.csv"):
        """Save analysis results to CSV."""
        import csv
        with open(output_file, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

        print(f"Results saved to {output_file}")

    def visualize_sample(self, sample_idx):
        """Visualize a specific frame."""
        img = self.images[sample_idx]
        plt.imshow(img, cmap="viridis")
        plt.title(f"Frame {sample_idx + 1}")
        plt.colorbar(label="Intensity")
        plt.savefig(f"plot_reports/sample_frame_{sample_idx + 1}.png", dpi=150, bbox_inches="tight")
        plt.show()


# Execute the algorithm
if __name__ == "__main__":
    analysis = FrameAnalysis(folders=folders)
    analysis.load_images()

    results = analysis.analyze_images()
    analysis.save_results(results)

    # Visualize a sample
    analysis.visualize_sample(sample_idx=10)
