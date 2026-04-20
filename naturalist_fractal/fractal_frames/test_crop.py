"""
test_crop.py — Quick Crop Calibrator
=====================================
Outputs only 2 test WebP frames so you can rapidly iterate
on CROP_RATIOS until the result is pixel-perfect (no white border).

Run:  python test_crop.py
Output: test_crop_A.webp (frame 1, early fractal)
        test_crop_B.webp (frame 501, complex fractal)

Once happy, copy the CROP_RATIOS values into prepare_web_frames.py.
"""

import os
from PIL import Image, ImageDraw, ImageFont

# Fixed pixel offsets — same absolute crop regardless of image width:
# Different frame batches: frame_001 is 1481px wide, frame_501 is 1454px wide.
# Ratios give inconsistent absolute positions; offsets from each edge don't.
CROP_PX = {
    "left":   111,    # px from left  — start of fractal plot
    "right":  242,    # px from right — colorbar + label width
    "top":    161,    # px from top   — below title text
    "bottom": 150,    # px from bottom — above x-axis label
}

OUTPUT_SIZE = (800, 800)
WEBP_QUALITY = 82

# Source frames to test with
TEST_FRAMES = {
    "A": os.path.join("frames", "frame_001.png"),    # early / smooth
    "B": os.path.join("frames2", "frame_501.png"),   # complex / detailed
}

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


def crop_and_convert(label, src_path):
    if not os.path.exists(src_path):
        print(f"  [SKIP] Not found: {src_path}")
        return

    with Image.open(src_path) as img:
        w, h = img.size
        left   = CROP_PX["left"]
        right  = w - CROP_PX["right"]
        top    = CROP_PX["top"]
        bottom = h - CROP_PX["bottom"]

        cropped = img.crop((left, top, right, bottom))
        resized = cropped.resize(OUTPUT_SIZE, Image.Resampling.LANCZOS)

        out_path = os.path.join(OUTPUT_DIR, f"test_crop_{label}.webp")
        resized.save(out_path, "WEBP", quality=WEBP_QUALITY)

        crop_w = right - left
        crop_h = bottom - top
        print(f"  [test_crop_{label}.webp] src={w}x{h}  crop=({left},{top})->({right},{bottom})  "
              f"crop_size={crop_w}x{crop_h}  -> {OUTPUT_SIZE[0]}x{OUTPUT_SIZE[1]}")
        print(f"  Saved: {out_path}")


def main():
    print("=" * 60)
    print("  Crop Calibrator - 2 Test Frames")
    print("=" * 60)
    print()
    print(f"  CROP_PX: left={CROP_PX['left']}, right={CROP_PX['right']}, "
          f"top={CROP_PX['top']}, bottom={CROP_PX['bottom']}")
    print()

    for label, path in TEST_FRAMES.items():
        crop_and_convert(label, path)
        print()

    print("Open test_crop_A.webp and test_crop_B.webp to inspect.")
    print("Adjust CROP_RATIOS above and re-run until perfect.")
    print("=" * 60)


if __name__ == "__main__":
    main()
