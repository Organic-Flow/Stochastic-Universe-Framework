import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import json

os.makedirs("csv", exist_ok=True)
os.makedirs("plot_reports", exist_ok=True)
os.makedirs("json_reports", exist_ok=True)


# Load images from frame folders
def load_images_from_folders(folder_paths):
    images = []
    stochastic_factors = []
    # Adjust base_path to go back to fractal_frames
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
                        # Extract σ factor from filename, e.g., frame_0.003.png
                        factor = float(filename.split('_')[1].replace('.png', ''))
                        stochastic_factors.append(factor)
                    except:
                        # Fallback for different naming conventions
                        factor = float(filename.split('.')[0].replace('frame', ''))
                        stochastic_factors.append(factor)
    return images, stochastic_factors


# Extract geometric parameters (angle, area, perimeter) from X-shape contours
def analyze_geometry(images, stochastic_factors):
    results = []
    for img, factor in zip(images, stochastic_factors):
        _, binary = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int64(box)

            angle = rect[2]
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)

            results.append({
                "stochastic_factor": factor,
                "angle": float(angle),
                "area": float(area),
                "perimeter": float(perimeter)
            })
    return results


# Visualize angle, area, and perimeter evolution across σ values
def visualize_geometry(results):
    factors = [res["stochastic_factor"] for res in results]
    angles = [res["angle"] for res in results]
    areas = [res["area"] for res in results]
    perimeters = [res["perimeter"] for res in results]

    plt.figure(figsize=(10, 6))
    plt.plot(factors, angles, label="Angle of X (degrees)")
    plt.xlabel("Stochastic Factor")
    plt.ylabel("Angle (degrees)")
    plt.title("Angle Evolution of 'X' Shape")
    plt.legend()
    plt.savefig("plot_reports/geometry_angle_evolution.png", dpi=150, bbox_inches="tight")
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(factors, areas, label="Area of X")
    plt.plot(factors, perimeters, label="Perimeter of X")
    plt.xlabel("Stochastic Factor")
    plt.ylabel("Value")
    plt.title("Area and Perimeter Evolution of 'X' Shape")
    plt.legend()
    plt.savefig("plot_reports/geometry_area_perimeter_evolution.png", dpi=150, bbox_inches="tight")
    plt.show()

    # Save to JSON
    json_report_data = {
        "name": "Geometry Analysis",
        "factors": factors,
        "angles": angles,
        "areas": areas,
        "perimeters": perimeters
    }
    json_report_file = "json_reports/geometry_analysis.json"
    with open(json_report_file, "w", encoding="utf-8") as f:
        json.dump(json_report_data, f, indent=2, ensure_ascii=False)
    print(f"JSON report saved to {json_report_file}")


if __name__ == "__main__":
    # Prefer raw grayscale frames (cv2.imwrite output) over matplotlib figures.
    raw_folders = ["raw_frames", "raw_frames1", "raw_frames2", "raw_frames3", "raw_frames4"]
    std_folders = ["frames", "frames1", "frames2", "frames3", "frames4"]
    
    # Check which folders exist relative to fractal_frames path
    base_path = "../../../fractal_frames/"
    folder_paths = raw_folders if all(os.path.isdir(os.path.join(base_path, f)) for f in raw_folders) else std_folders
    
    if folder_paths == raw_folders:
        print("Using raw grayscale frames for accurate geometric analysis.")
    else:
        print("Warning: raw_frames not found or incomplete. Using standard figure PNGs.")
    
    images, stochastic_factors = load_images_from_folders(folder_paths)
    results = analyze_geometry(images, stochastic_factors)
    visualize_geometry(results)
