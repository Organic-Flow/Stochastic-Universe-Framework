import os
import numpy as np
import cv2  # Install with: pip install opencv-python
import pandas as pd
from tqdm import tqdm  # For progress bar

os.makedirs("csv", exist_ok=True)
os.makedirs("plot_reports", exist_ok=True)


# List of folders containing PNG
base_path = "../../../fractal_frames/"
folders = ["frames", "frames1", "frames2", "frames3", "frames4"]

# List for storing data
data = []


# Function to read and analyze images
def analyze_image(image_path):
    """Analyzes an image and extracts features."""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Read the image in grayscale
    if img is None:
        return None, None
    avg_intensity = np.mean(img) / 255.0  # Normalized average intensity (0-1)
    max_intensity = np.max(img) / 255.0  # Normalized maximum intensity (0-1)
    return avg_intensity, max_intensity


# Analyze all images
for folder in folders:
    folder_path = os.path.join(base_path, folder)
    print(f"Analyzing folder: {folder_path}")
    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} does not exist. Skipping.")
        continue

    # Traverse PNG files in the folder
    files = [f for f in os.listdir(folder_path) if f.endswith(".png")]
    for file_name in tqdm(files):
        file_path = os.path.join(folder_path, file_name)
        try:
            # Extract frame number, handle different naming conventions if necessary
            # Assuming format: frame_NUMBER.png or similar
            parts = file_name.split('_')
            if len(parts) > 1:
                frame_number = int(parts[1].split('.')[0])
            else:
                frame_number = int(file_name.split('.')[0].replace('frame', ''))
                
            avg_intensity, max_intensity = analyze_image(file_path)
            if avg_intensity is None:
                continue

            # Save results
            data.append({
                "Frame": frame_number,
                "Folder": folder,
                "Avg Intensity": avg_intensity,
                "Max Intensity": max_intensity
            })
        except Exception as e:
            print(f"Error processing {file_name}: {e}")

# Convert data to DataFrame
df = pd.DataFrame(data)

# Sort data based on frames
df = df.sort_values(by=["Folder", "Frame"]).reset_index(drop=True)

# Save to new CSV
output_csv = "csv/new_frame_analysis.csv"
df.to_csv(output_csv, index=False)
print(f"Analysis completed. Results saved in {output_csv}.")
