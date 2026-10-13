# ============================================================================
# Course: Multimedia Systems & Programming
# Session: 04 - Digital Images with OpenCV
# Instructor: Eng. Muhammad Ali Abdul Kareem — Sinai University
# ============================================================================
# Description:
# Hands-on Python script covering the 6 core image processing operations 
# taught in Session 04 slides:
#   1. Input image (cv2.imread & path check)
#   2. Grayscale conversion (cv2.cvtColor)
#   3. Binary thresholding (cv2.threshold)
#   4. Resizing dimensions (cv2.resize)
#   5. Orthogonal rotation (cv2.rotate)
#   6. Display image (cv2.imshow / Colab cv2_imshow)
# Plus the Complete Pipeline Script & Student Practice Task Solution.
# ============================================================================

import os
import cv2
import numpy as np

# Detect environment: Google Colab vs Local Desktop
try:
    from google.colab.patches import cv2_imshow
    IS_COLAB = True
except ImportError:
    IS_COLAB = False

def show_image(title, image):
    """Unified display helper that works on both Google Colab and Local Python."""
    if IS_COLAB:
        print(f"\n--- [Display: {title}] ---")
        cv2_imshow(image)
    else:
        cv2.imshow(title, image)
        print(f"Showing '{title}'. Press any key in the image window to continue...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()


print("==================================================")
print("  Session 04: Digital Images with OpenCV (cv2)   ")
print("==================================================\n")

# ============================================================================
# 0. IMAGE PATH SETUP & FALLBACK TEST IMAGE
# ============================================================================
# In Google Colab, upload your image file and it will be located in '/content/'
IMAGE_PATH = "/content/image_name.jpg"

# Fallback check: if running locally or image hasn't been uploaded yet,
# create a clean sample image so students can execute the code immediately!
if not os.path.exists(IMAGE_PATH):
    local_sample = "image_name.jpg"
    if not os.path.exists(local_sample):
        # Create a sample colorful test pattern (240x320x3)
        sample = np.zeros((240, 320, 3), dtype=np.uint8)
        # Background gradient
        for y in range(240):
            sample[y, :] = [int(180 - y * 0.4), int(100 + y * 0.5), int(50 + y * 0.7)]
        # Bright geometric shapes to test grayscale and thresholding
        cv2.circle(sample, (160, 110), 60, (0, 215, 255), -1)   # Yellow Sun/Circle
        cv2.rectangle(sample, (40, 150), (280, 225), (60, 180, 75), -1) # Green Ground
        cv2.putText(sample, "Sinai Univ", (75, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
        cv2.imwrite(local_sample, sample)
    IMAGE_PATH = local_sample
    print(f"[Info] Running with sample image: '{IMAGE_PATH}'")


# ============================================================================
# 1. READ IMAGE & THE NUMPY ARRAY (Core Idea & Step 1)
# ============================================================================
# cv2.imread turns a file into a NumPy array of shape (Height, Width, 3).
# Important: OpenCV loads colors in BGR order (Blue, Green, Red), NOT RGB!
img = cv2.imread(IMAGE_PATH)

if img is None:
    print("Error: image not found! Check the path.")
    exit(1)

h, w, c = img.shape
print("\n[Step 1: Input Image & Array Properties]")
print(f"   • img.shape  : {img.shape}  -> (Height={h}, Width={w}, Channels={c})")
print(f"   • Data Type  : {img.dtype}  -> (8-bit unsigned integer: 0..255)")
print(f"   • Top-Left   : img[0, 0] = {img[0, 0]}  -> [Blue, Green, Red]")


# ============================================================================
# 2. CONVERT RGB/BGR TO GRAYSCALE (Step 2)
# ============================================================================
# cv2.cvtColor converts between color spaces.
# Color image has 3 channels (B, G, R); Grayscale has only 1 channel: (H, W).
# Intensity ranges from 0 (pure black) to 255 (pure white).
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

print("\n[Step 2: Grayscale Conversion]")
print(f"   • gray.shape : {gray.shape}  -> (Height={h}, Width={w}) [1 channel]")
print(f"   • Pixel [0,0]: {gray[0, 0]} intensity level (0..255)")


# ============================================================================
# 3. CONVERT GRAYSCALE TO BINARY (Step 3: Thresholding)
# ============================================================================
# cv2.threshold turns a single-channel grayscale image into pure black & white.
# Rule: If gray[y, x] > 127 => 255 (White), otherwise => 0 (Black).
# Returns two values: the threshold cutoff (_) and the resulting binary image.
_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

print("\n[Step 3: Binary Thresholding]")
print(f"   • binary.shape : {binary.shape}")
print(f"   • Unique values: {np.unique(binary)} (Only 0 and 255)")


# ============================================================================
# 4. RESIZE IMAGE (Step 4)
# ============================================================================
# cv2.resize changes image dimensions.
# TRAP from slides: img.shape is (Height, Width), but cv2.resize takes (Width, Height)!
new_width = 300
new_height = 300
resized = cv2.resize(img, (new_width, new_height))

print("\n[Step 4: Resize Image]")
print(f"   • Target size  : (Width={new_width}, Height={new_height})")
print(f"   • resized.shape: {resized.shape} -> (Height={resized.shape[0]}, Width={resized.shape[1]}, Channels={resized.shape[2]})")


# ============================================================================
# 5. ROTATE IMAGE (Step 5)
# ============================================================================
# cv2.rotate turns the image by fixed orthogonal angles without distortion.
# Options:
#   • cv2.ROTATE_90_CLOCKWISE        (swaps height and width)
#   • cv2.ROTATE_180                 (keeps height and width)
#   • cv2.ROTATE_90_COUNTERCLOCKWISE (or 270 degrees)
rotated_90 = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
rotated_180 = cv2.rotate(img, cv2.ROTATE_180)

print("\n[Step 5: Rotate Image]")
print(f"   • Original shape  : {img.shape}")
print(f"   • Rotated 90° CW  : {rotated_90.shape} (H and W are swapped)")
print(f"   • Rotated 180°    : {rotated_180.shape} (H and W are preserved)")


# ============================================================================
# 6. SHOW IMAGE (Step 6)
# ============================================================================
# Local Python uses:
#   cv2.imshow('Title', img)
#   cv2.waitKey(0)           # waits forever for a key press
#   cv2.destroyAllWindows()  # closes windows and frees memory
#
# Google Colab cannot open desktop windows, so we use:
#   from google.colab.patches import cv2_imshow
#   cv2_imshow(img)
print("\n[Step 6: Displaying Images]")
show_image("Original Image (BGR)", img)
show_image("Grayscale Image (cv2.COLOR_BGR2GRAY)", gray)
show_image("Binary Image (Threshold = 127)", binary)
show_image("Resized Image (300x300)", resized)
show_image("Rotated 90 CW", rotated_90)


# ============================================================================
# 7. ALL TOGETHER: THE COMPLETE SCRIPT (Slide 13)
# ============================================================================
print("\n" + "="*50)
print("  Slide 13: Complete Colab-Ready Pipeline Script  ")
print("="*50)
complete_code_sample = """
import cv2
from google.colab.patches import cv2_imshow

# 1. read the image (uploaded to /content)
img = cv2.imread('/content/image_name.jpg')

if img is None:
    print("Error: image not found! Check the path.")
else:
    # 2. grayscale   3. binary
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # 4. resize   5. rotate
    resized = cv2.resize(img, (300, 300))
    rotated = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

    # 6. show (cv2_imshow replaces cv2.imshow on Colab)
    cv2_imshow(img)
    cv2_imshow(gray)
    cv2_imshow(binary)
    cv2_imshow(resized)
    cv2_imshow(rotated)
"""
print(complete_code_sample.strip())


# ============================================================================
# 8. STUDENT PRACTICE TASK & SOLUTION (Slide 14)
# ============================================================================
# Requirements from Slide 14:
#   1. Change threshold to 100 and compare binary image with 127
#   2. Resize to (150, 150) and print resized.shape
#   3. Rotate by 180 degrees and print rotated.shape, then try 90 degrees
print("\n" + "="*50)
print("  Slide 14: Student Task Reference Solution       ")
print("="*50)

# 1. Threshold at 100 vs 127
_, binary_100 = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
white_at_100 = np.mean(binary_100 == 255) * 100
white_at_127 = np.mean(binary == 255) * 100
print(f"Task 1: Threshold = 100 -> {white_at_100:.1f}% white pixels (more white than T=127: {white_at_127:.1f}%)")

# 2. Resize to (150, 150)
task_resized = cv2.resize(img, (150, 150))
print(f"Task 2: resized.shape   -> {task_resized.shape} (Width=150, Height=150)")

# 3. Rotate 180 degrees vs 90 degrees
task_rot_180 = cv2.rotate(img, cv2.ROTATE_180)
print(f"Task 3: rotated 180°    -> {task_rot_180.shape} (Shape preserved)")
print(f"        rotated 90° CW  -> {rotated_90.shape} (Shape transposed)")

print("\n✓ Session 04 Python code executed successfully!")
