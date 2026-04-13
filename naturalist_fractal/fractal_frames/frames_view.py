import os
import time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Folder with images
image_folder = "frames2"

# Check if folder exists
if not os.path.exists(image_folder):
    print(f"The folder {image_folder} does not exist. Make sure the images have been created.")
    exit()

# List of images sorted alphabetically
image_files = sorted([os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(".png")])

# Check if images exist
if not image_files:
    print(f"The folder {image_folder} does not contain PNG images.")
    exit()

# Window preparation
fig, ax = plt.subplots(figsize=(12, 12))
ax.axis('off')  # Remove axes

# Display images one by one
for image_file in image_files:
    print(f"Displaying: {image_file}")

    # Load image
    img = mpimg.imread(image_file)

    # Update window
    ax.imshow(img)
    plt.pause(1)  # Wait 5 seconds

plt.close()
