"""
Prepare Web Frames — PNG to WebP Converter
============================================
Aggregates all fractal PNG frames from frames/, frames1/, frames2/, frames3/, frames4/
and converts them to optimized WebP format for the Image Sequence Scrubbing viewer.

Output: web_frames/ directory in ../../website/ with 0000.webp to 0999.webp
"""

import os
import sys
from PIL import Image

# ── Configuration ──
FRAME_DIRS = ["frames", "frames1", "frames2", "frames3", "frames4"]
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "website", "web_frames")
TARGET_SIZE = (800, 800)   # Web-optimized resolution
WEBP_QUALITY = 82          # High quality, good compression

# Crop matplotlib chrome (axes, title, colorbar) — pixel-perfect calibration.
#
# IMPORTANT: Different frame batches have different IMAGE WIDTHS (1454px vs 1481px)
# but the same HEIGHT (1423px). Using fixed pixel offsets from each edge ensures
# consistent cropping regardless of which batch a frame comes from.
#
# Calibrated by pixel-scanning frame_001.png (1481px) and frame_501.png (1454px):
CROP_PX = {
    "left":   111,    # px from left  — start of fractal plot (past y-axis ticks)
    "right":  242,    # px from right — colorbar + label width (constant offset)
    "top":    161,    # px from top   — below title text
    "bottom": 150,    # px from bottom — above x-axis label (1423-1273=150)
}

def collect_all_frames(base_dir, frame_dirs):
    """
    Collect all PNG frames from multiple directories and return them
    sorted by their frame number (frame_001.png -> 1).
    """
    all_frames = {}  # frame_number -> full_path

    for fdir in frame_dirs:
        folder = os.path.join(base_dir, fdir)
        if not os.path.isdir(folder):
            print(f"  [SKIP] Directory not found: {fdir}")
            continue

        pngs = [f for f in os.listdir(folder) if f.endswith('.png') and f.startswith('frame_')]
        for fname in pngs:
            # Extract frame number: "frame_801.png" -> 801
            try:
                num = int(fname.replace("frame_", "").replace(".png", ""))
                all_frames[num] = os.path.join(folder, fname)
            except ValueError:
                continue

    return all_frames


def crop_matplotlib_chrome(img):
    """
    Crop the matplotlib axes, title, colorbar, and labels to expose
    only the raw fractal plot area.

    Uses fixed pixel offsets (not ratios) for left/right so that frames
    from different batches with different widths are cropped consistently.
    """
    w, h = img.size
    left   = CROP_PX["left"]
    right  = w - CROP_PX["right"]
    top    = CROP_PX["top"]
    bottom = h - CROP_PX["bottom"]
    return img.crop((left, top, right, bottom))


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 60)
    print("  Naturalist Fractal - Web Frame Preparation")
    print("=" * 60)
    print()

    # Step 1: Collect all frames
    print("[1/3] Scanning frame directories...")
    all_frames = collect_all_frames(base_dir, FRAME_DIRS)
    total = len(all_frames)
    print(f"       Found {total} unique frames across {len(FRAME_DIRS)} directories")
    print()

    if total == 0:
        print("ERROR: No frames found! Check that frame directories exist.")
        sys.exit(1)

    # Step 2: Sort by frame number and create sequential index
    sorted_numbers = sorted(all_frames.keys())
    print(f"[2/3] Frame range: {sorted_numbers[0]} -> {sorted_numbers[-1]}")
    print(f"       Stochastic Factor: {0.803 + (sorted_numbers[0] - 1) * 0.001:.3f} -> "
          f"{0.803 + (sorted_numbers[-1] - 1) * 0.001:.3f}")
    print()

    # Step 3: Convert to WebP
    print(f"[3/3] Converting {total} PNG -> WebP ({TARGET_SIZE[0]}x{TARGET_SIZE[1]}, quality={WEBP_QUALITY})...")
    print(f"       Output: {os.path.abspath(OUTPUT_DIR)}")
    print()

    for idx, frame_num in enumerate(sorted_numbers):
        src_path = all_frames[frame_num]

        with Image.open(src_path) as img:
            # Crop matplotlib decorations
            img_cropped = crop_matplotlib_chrome(img)

            # Resize to target web dimensions
            img_resized = img_cropped.resize(TARGET_SIZE, Image.Resampling.LANCZOS)

            # Save as WebP with sequential naming: 0000.webp, 0001.webp, ...
            out_name = f"{idx:04d}.webp"
            img_resized.save(
                os.path.join(OUTPUT_DIR, out_name),
                "WEBP",
                quality=WEBP_QUALITY,
                method=6  # Slowest but best compression
            )

        if idx % 50 == 0 or idx == total - 1:
            pct = ((idx + 1) / total) * 100
            print(f"       [{pct:5.1f}%] Frame {frame_num:4d} -> {out_name}  "
                  f"(s = {0.803 + (frame_num - 1) * 0.001:.3f})")

    # Summary
    total_size_mb = sum(
        os.path.getsize(os.path.join(OUTPUT_DIR, f))
        for f in os.listdir(OUTPUT_DIR) if f.endswith('.webp')
    ) / (1024 * 1024)

    print()
    print("=" * 60)
    print(f"  [OK] Done! {total} frames converted successfully")
    print(f"  [OK] Total output size: {total_size_mb:.1f} MB")
    print(f"  [OK] Average per frame: {total_size_mb / total * 1024:.0f} KB")
    print(f"  [OK] Output: {os.path.abspath(OUTPUT_DIR)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
