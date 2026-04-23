import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import json
from Analysis_of_Stochastic_Factor import analyze_stochastic_effect

os.makedirs("csv", exist_ok=True)
os.makedirs("plot_reports", exist_ok=True)
os.makedirs("json_reports", exist_ok=True)


# Step 1: Load images from frame folders
def load_images_from_folders(folder_paths):
    images = []
    stochastic_factors = []
    base_path = "../../../fractal_frames/"
    for folder_name in folder_paths:
        folder_path = os.path.join(base_path, folder_name)
        if not os.path.exists(folder_path):
            continue
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith('.png'):
                img = cv2.imread(os.path.join(folder_path, filename), cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    images.append(img)
                    try:
                        factor = float(filename.split('_')[1].replace('.png', ''))
                        stochastic_factors.append(factor)
                    except:
                        factor = float(filename.split('.')[0].replace('frame', ''))
                        stochastic_factors.append(factor)
    return images, stochastic_factors


# Step 2: Compute contour curvature for each frame
def calculate_curvature(images, stochastic_factors):
    curvature_results = []
    for img, factor in zip(images, stochastic_factors):
        _, binary = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            curvature = 0
            if len(contour) > 2:
                for i in range(1, len(contour) - 1):
                    prev_point = contour[i - 1][0]
                    curr_point = contour[i][0]
                    next_point = contour[i + 1][0]

                    v1 = np.array(curr_point) - np.array(prev_point)
                    v2 = np.array(next_point) - np.array(curr_point)
                    
                    norm1 = np.linalg.norm(v1)
                    norm2 = np.linalg.norm(v2)
                    
                    if norm1 > 0 and norm2 > 0:
                        cos_angle = np.dot(v1, v2) / (norm1 * norm2)
                        cos_angle = np.clip(cos_angle, -1.0, 1.0)
                        angle = np.arccos(cos_angle)
                        curvature += angle

            curvature_results.append({
                "stochastic_factor": factor,
                "curvature": float(curvature / len(contour)) if len(contour) > 0 else 0
            })
    return curvature_results


# Step 3: Visualize raw curvature scatter across σ values
def visualize_curvature(curvature_results):
    factors = [res["stochastic_factor"] for res in curvature_results]
    curvatures = [res["curvature"] for res in curvature_results]

    plt.figure(figsize=(10, 6))
    plt.plot(factors, curvatures, label="Average Curvature")
    plt.xlabel("Stochastic Factor")
    plt.ylabel("Curvature")
    plt.title("Curvature Evolution of 'X' Shape")
    plt.legend()
    plt.savefig("plot_reports/curvature_evolution.png", dpi=150, bbox_inches="tight")
    plt.show()

    # Save to JSON
    json_report_data = {
        "name": "Curvature Analysis",
        "factors": factors,
        "curvatures": curvatures
    }
    json_report_file = "json_reports/curvature_analysis.json"
    with open(json_report_file, "w", encoding="utf-8") as f:
        json.dump(json_report_data, f, indent=2, ensure_ascii=False)
    print(f"JSON report saved to {json_report_file}")


if __name__ == "__main__":
    # Prefer raw grayscale frames (cv2.imwrite output) over matplotlib figures.
    raw_folders = ["raw_frames", "raw_frames1", "raw_frames2", "raw_frames3", "raw_frames4"]
    std_folders = ["frames", "frames1", "frames2", "frames3", "frames4"]
    
    base_path = "../../../fractal_frames/"
    folder_paths = raw_folders if all(os.path.isdir(os.path.join(base_path, f)) for f in raw_folders) else std_folders
    
    if folder_paths == raw_folders:
        print("Using raw grayscale frames for accurate geometric analysis.")
    else:
        print("Warning: raw_frames not found or incomplete. Using standard figure PNGs.")
    
    images, stochastic_factors = load_images_from_folders(folder_paths)
    curvature_results = calculate_curvature(images, stochastic_factors)
    visualize_curvature(curvature_results)
    analyze_stochastic_effect(curvature_results)
