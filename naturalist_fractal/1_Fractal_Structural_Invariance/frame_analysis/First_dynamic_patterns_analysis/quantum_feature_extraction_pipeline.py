import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import json
import sys
import csv

# Add the parent directory to sys.path to import meta_qubit
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
try:
    from meta_qubit import MetaQubit
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from meta_qubit import MetaQubit

# Output directories
os.makedirs("csv", exist_ok=True)
os.makedirs("plot_reports", exist_ok=True)
os.makedirs("json_reports", exist_ok=True)

# Locate frame folders
base_path = "../../../fractal_frames/"
folders = ["frames", "frames1", "frames2", "frames3", "frames4"]

class FrameAnalysis:
    def __init__(self, base_path, folders):
        self.base_path = base_path
        self.folders = folders
        self.meta_qubit = MetaQubit(num_qubits=4)

    def run_pipeline(self):
        """Process images one by one to save memory."""
        results = []
        frame_count = 0
        
        # Get all file paths first
        all_files = []
        for folder in self.folders:
            folder_path = os.path.join(self.base_path, folder)
            if not os.path.exists(folder_path):
                print(f"Warning: Folder {folder_path} not found.")
                continue
            files = sorted([os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".png")])
            all_files.extend(files)
            
        print(f"Starting analysis of {len(all_files)} images...")
        
        for idx, img_path in enumerate(all_files):
            try:
                # Load and process ONE image
                with Image.open(img_path) as img_raw:
                    img = np.array(img_raw.convert("L")) / 255.0
                
                avg_intensity = np.mean(img)
                max_intensity = np.max(img)

                # Run MetaQubit circuit
                quantum_result = self.meta_qubit.run_circuit()
                coherence_score = np.sum(quantum_result) / len(quantum_result)

                results.append({
                    "Frame": idx + 1,
                    "Avg Intensity": float(avg_intensity),
                    "Max Intensity": float(max_intensity),
                    "Quantum Coherence": float(coherence_score)
                })

                if (idx + 1) % 50 == 0:
                    print(f"Progress: {idx + 1}/{len(all_files)} frames analyzed...")
                
                # Save a sample plot for the 10th frame
                if idx == 10:
                    plt.figure(figsize=(8, 8))
                    plt.imshow(img, cmap="viridis")
                    plt.title(f"Frame {idx + 1}")
                    plt.colorbar(label="Intensity")
                    plt.savefig(f"plot_reports/sample_frame_{idx + 1}.png", dpi=150, bbox_inches="tight")
                    plt.close()
                    
            except Exception as e:
                print(f"Error processing {img_path}: {e}")

        # Save Results
        self.save_results(results)

    def save_results(self, results, output_file="csv/frame_analysis_results.csv"):
        if not results:
            return
            
        with open(output_file, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        print(f"Results saved to {output_file}")
        
        json_report_data = {
            "phase": "Quantum Feature Extraction",
            "name": "Quantum Analysis Pipeline",
            "results": results
        }
        json_report_file = "json_reports/quantum_feature_extraction.json"
        with open(json_report_file, "w", encoding="utf-8") as f:
            json.dump(json_report_data, f, indent=2, ensure_ascii=False)
        print(f"JSON report saved to {json_report_file}")

if __name__ == "__main__":
    analysis = FrameAnalysis(base_path=base_path, folders=folders)
    analysis.run_pipeline()
