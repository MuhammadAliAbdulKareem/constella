# ============================================================================
# Course: Multimedia Systems & Programming
# Session: 04 - Digital Images with OpenCV
# Instructor: Eng. Muhammad Ali Abdul Kareem — Sinai University
# ============================================================================

import cv2
import numpy as np

# Colab display compatibility check
try:
    from google.colab.patches import cv2_imshow
    IS_COLAB = True
except ImportError:
    IS_COLAB = False


# ============================================================================
# 1. READ IMAGE & NUMPY ARRAY PROPERTIES (cv2.imread)
# ============================================================================
# Path to image file (On Colab: upload file to /content/image_name.jpg)
image_path = "image_name.jpg"

# 1. Read the image from disk (OpenCV loads in BGR order: Blue, Green, Red)
img = cv2.imread(image_path)

# Always check if the image loaded successfully
if img is None:
    print(f"Error: Could not load image from '{image_path}'. Check the path!")
else:
    # An image is a 3D NumPy array: (Height, Width, Channels)
    print("=== 1. Input Image Properties ===")
    print("Image shape :", img.shape)       # (H, W, 3)
    print("Data type   :", img.dtype)       # uint8 (0 to 255)
    print("Pixel [0, 0]:", img[0, 0])       # [B, G, R] values of top-left pixel


# ============================================================================
# 2. CONVERT RGB/BGR TO GRAYSCALE (cv2.cvtColor)
# ============================================================================
# Converts 3 color channels (B, G, R) into 1 luminance channel (H, W)
# Gray = 0.299*R + 0.587*G + 0.114*B
if img is not None:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print("\n=== 2. Grayscale Conversion ===")
    print("Gray shape :", gray.shape)       # (H, W) - single channel
    print("Gray pixel :", gray[0, 0])       # Single intensity value (0 to 255)


# ============================================================================
# 3. CONVERT GRAYSCALE TO BINARY (cv2.threshold)
# ============================================================================
# Turns grayscale image into binary (pure black: 0, pure white: 255)
# Pixel > 127 becomes 255; otherwise 0
if img is not None:
    threshold_value = 127
    max_value = 255
    _, binary = cv2.threshold(gray, threshold_value, max_value, cv2.THRESH_BINARY)
    print("\n=== 3. Binary Thresholding ===")
    print("Binary shape :", binary.shape)
    print("Binary values: only 0 and 255")


# ============================================================================
# 4. RESIZE IMAGE (cv2.resize)
# ============================================================================
# Changes dimensions to (Width, Height). Note: order is (Width, Height), not (H, W)!
if img is not None:
    new_size = (300, 300)  # (Width, Height)
    resized = cv2.resize(img, new_size)
    print("\n=== 4. Resizing Image ===")
    print("Resized shape:", resized.shape)  # (300, 300, 3)


# ============================================================================
# 5. ROTATE IMAGE (cv2.rotate)
# ============================================================================
# Turns image by fixed right angles:
#   • cv2.ROTATE_90_CLOCKWISE        (swaps Height and Width)
#   • cv2.ROTATE_180                 (keeps Height and Width)
#   • cv2.ROTATE_90_COUNTERCLOCKWISE (270 degrees)
if img is not None:
    rotated_90 = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    rotated_180 = cv2.rotate(img, cv2.ROTATE_180)
    print("\n=== 5. Rotating Image ===")
    print("Rotated 90° shape :", rotated_90.shape)   # Height and Width swapped
    print("Rotated 180° shape:", rotated_180.shape)  # Original shape kept


# ============================================================================
# 6. DISPLAY IMAGES (cv2.imshow / Colab cv2_imshow)
# ============================================================================
if img is not None:
    print("\n=== 6. Displaying Images ===")
    if IS_COLAB:
        cv2_imshow(img)
        cv2_imshow(gray)
        cv2_imshow(binary)
        cv2_imshow(resized)
        cv2_imshow(rotated_90)
    else:
        cv2.imshow("1. Original (BGR)", img)
        cv2.imshow("2. Grayscale", gray)
        cv2.imshow("3. Binary Threshold", binary)
        cv2.imshow("4. Resized (300x300)", resized)
        cv2.imshow("5. Rotated 90 CW", rotated_90)
        print("Press any key in image windows to close them...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()


# ============================================================================
# 7. STUDENT PRACTICE TASK SOLUTION
# ============================================================================
# Task Requirements:
#   1. Change threshold to 100 and compare binary image with 127
#   2. Resize to (150, 150) and print resized.shape
#   3. Rotate by 180 degrees and print rotated.shape, then try 90 degrees
if img is not None:
    print("\n=== 7. Student Practice Task Solution ===")

    # 1. Threshold at 100
    _, binary_100 = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    print("• Binary (T=100) created -> lower threshold = more white pixels")

    # 2. Resize to (150, 150)
    task_resized = cv2.resize(img, (150, 150))
    print("• task_resized.shape:", task_resized.shape)  # (150, 150, 3)

    # 3. Rotate 180 vs 90 degrees
    task_rotated_180 = cv2.rotate(img, cv2.ROTATE_180)
    task_rotated_90 = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    print("• task_rotated_180.shape:", task_rotated_180.shape)  # (H, W, 3)
    print("• task_rotated_90.shape :", task_rotated_90.shape)   # (W, H, 3)
