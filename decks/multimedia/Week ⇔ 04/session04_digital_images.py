# ============================================================================
# Course: Multimedia Systems & Programming
# Session: 04 - Digital Images in Python: Matrix Grid, Transformations & Filtering
# Instructor: Eng. Muhammad Ali Abdul Kareem — Sinai University
# ============================================================================

import cv2
import numpy as np
import matplotlib.pyplot as plt

print("==================================================")
print("  Session 04: Digital Image Processing in Python  ")
print("==================================================\n")

# ============================================================================
# HELPER: Generate a clean synthetic test image (if no file is present)
# ============================================================================
def generate_sample_image(height=160, width=200):
    """
    Creates a colorful synthetic landscape image with sky, sun, mountains,
    and grass to clearly demonstrate colors, rotation, and grayscale.
    """
    img = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Sky (Blue gradient in RGB, Blue channel in BGR)
    for y in range(height):
        # BGR format: [B, G, R]
        b = int(220 - y * 0.4)
        g = int(140 - y * 0.3)
        r = int(50 + y * 0.2)
        img[y, :] = [b, g, r]
        
    # Sun (Yellow circle)
    cv2.circle(img, (width - 45, 45), 26, (0, 215, 255), -1) # BGR Yellow
    
    # Mountains (Triangles)
    pts1 = np.array([[10, height - 30], [80, 50], [150, height - 30]], np.int32)
    pts2 = np.array([[90, height - 30], [150, 65], [210, height - 30]], np.int32)
    cv2.fillPoly(img, [pts1], (80, 70, 110))
    cv2.fillPoly(img, [pts2], (95, 85, 130))
    
    # Grass ground (Green)
    cv2.rectangle(img, (0, height - 35), (width, height), (35, 150, 45), -1)
    
    return img

# Load image from disk or fallback to synthetic sample
img_bgr = generate_sample_image()

# ============================================================================
# 1. INPUT IMAGE (MATRIX REPRESENTATION & PROPERTIES)
# ============================================================================
# An image in Python/NumPy is a 3D Tensor of shape (Height, Width, Channels).
# Coordinates: img[row, col] -> y is row (Height), x is col (Width).
h, w, c = img_bgr.shape
print("1. Image Input & Matrix Properties:")
print(f"   - Dimensions (Shape) : {img_bgr.shape} (Height={h}, Width={w}, Channels={c})")
print(f"   - Data Type (dtype)  : {img_bgr.dtype} (8-bit unsigned integer: 0..255)")
print(f"   - Total Pixels       : {img_bgr.size // 3} pixels ({img_bgr.size} color bytes)")
print(f"   - Top-Left Pixel BGR : {img_bgr[0, 0]}")
print()

# ============================================================================
# 2. SHOW IMAGE & THE BGR vs RGB CHANNEL TRAP
# ============================================================================
# OpenCV loads images in BGR order (historical reason for IBM PC framegrabbers).
# Matplotlib and standard screens expect RGB order.
# If displayed directly without conversion, Red and Blue swap!
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

# Alternative NumPy slicing technique to invert channel order:
# img_rgb_slice = img_bgr[:, :, ::-1]

plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.imshow(img_bgr) # Incorrect: Blue and Red swapped
plt.title("2.a Wrong: Raw BGR in Matplotlib")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(img_rgb) # Correct: Converted to RGB
plt.title("2.b Correct: cv2.cvtColor(BGR ➔ RGB)")
plt.axis("off")
plt.tight_layout()
plt.show()

# ============================================================================
# 3. ROTATE (ORTHOGONAL & ARBITRARY AFFINE ANGLES)
# ============================================================================
# Method A: Fast 90-degree orthogonal steps (no interpolation needed)
rot_90_cw = cv2.rotate(img_rgb, cv2.ROTATE_90_CLOCKWISE)
rot_180   = cv2.rotate(img_rgb, cv2.ROTATE_180)

# Method B: Arbitrary angle rotation (Affine Transformation Matrix)
center = (w // 2, h // 2)
angle = 45 # degrees counter-clockwise
scale = 1.0
M = cv2.getRotationMatrix2D(center, angle, scale)
rot_45 = cv2.warpAffine(img_rgb, M, (w, h), borderMode=cv2.BORDER_REFLECT)

plt.figure(figsize=(12, 3.5))
plt.subplot(1, 4, 1); plt.imshow(img_rgb); plt.title("Original"); plt.axis("off")
plt.subplot(1, 4, 2); plt.imshow(rot_90_cw); plt.title("Rotate 90° CW"); plt.axis("off")
plt.subplot(1, 4, 3); plt.imshow(rot_180); plt.title("Rotate 180°"); plt.axis("off")
plt.subplot(1, 4, 4); plt.imshow(rot_45); plt.title("Affine 45° Matrix"); plt.axis("off")
plt.tight_layout()
plt.show()

# ============================================================================
# 4. RESIZE (DOWNSAMPLING, UPSAMPLING & INTERPOLATION)
# ============================================================================
# Notice the size order in cv2.resize: (Width, Height), opposite of shape (H, W)!
# Interpolation algorithms:
# - INTER_NEAREST: Fastest, blocky pixelated results.
# - INTER_LINEAR : Bilinear default, smooth and fast.
# - INTER_CUBIC  : Bicubic 4x4 neighborhood, highest quality for upsampling.
# - INTER_AREA   : Best pixel area relation for downsampling / shrinking.

# Downscale to 50%
downscaled = cv2.resize(img_rgb, (w // 2, h // 2), interpolation=cv2.INTER_AREA)

# Upscale back to 200% comparing Nearest Neighbor vs Bilinear
upscaled_nearest = cv2.resize(downscaled, (w * 2, h * 2), interpolation=cv2.INTER_NEAREST)
upscaled_linear  = cv2.resize(downscaled, (w * 2, h * 2), interpolation=cv2.INTER_LINEAR)

plt.figure(figsize=(10, 3.5))
plt.subplot(1, 3, 1); plt.imshow(downscaled); plt.title(f"Downscale 50% ({w//2}x{h//2})"); plt.axis("off")
plt.subplot(1, 3, 2); plt.imshow(upscaled_nearest); plt.title("Upscale (Nearest Neighbor)"); plt.axis("off")
plt.subplot(1, 3, 3); plt.imshow(upscaled_linear); plt.title("Upscale (Bilinear Linear)"); plt.axis("off")
plt.tight_layout()
plt.show()

# ============================================================================
# 5. CONVERT RGB TO GRAY LEVEL (LUMINANCE WEIGHTING)
# ============================================================================
# Why not simple average (R+G+B)/3?
# The human eye has far more Green cones than Red or Blue!
# ITU-R BT.601 formula:
#   Gray = 0.299 * R + 0.587 * G + 0.114 * B
# (Green gets ~59%, Red gets ~30%, Blue gets only ~11%)

# OpenCV implementation
gray_cv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

# Manual NumPy implementation from RGB channels
R = img_rgb[:, :, 0].astype(np.float32)
G = img_rgb[:, :, 1].astype(np.float32)
B = img_rgb[:, :, 2].astype(np.float32)
gray_manual = np.round(0.299 * R + 0.587 * G + 0.114 * B).astype(np.uint8)

print("5. Grayscale Conversion Metrics:")
print(f"   - Grayscale Shape : {gray_cv.shape} (2D Matrix, single intensity channel)")
print(f"   - Max diff between cv2 and manual formula: {np.max(np.abs(gray_cv.astype(int) - gray_manual.astype(int)))} levels")
print()

plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1); plt.imshow(img_rgb); plt.title("Original Color RGB"); plt.axis("off")
plt.subplot(1, 2, 2); plt.imshow(gray_cv, cmap='gray'); plt.title("Grayscale (Y = 0.3R + 0.59G + 0.11B)"); plt.axis("off")
plt.tight_layout()
plt.show()

# ============================================================================
# 6. CONVERT GRAY LEVEL TO BINARY (THRESHOLDING & MASKS)
# ============================================================================
# Binarization reduces 8-bit depth (256 levels) down to 1-bit (0 or 255).
# Rule: If Gray[r, c] > Threshold => 255 (White), else 0 (Black).

# OpenCV threshold function
threshold_val = 128
max_val = 255
ret, binary_cv = cv2.threshold(gray_cv, threshold_val, max_val, cv2.THRESH_BINARY)

# Manual NumPy boolean vectorization
binary_manual = np.where(gray_cv > threshold_val, 255, 0).astype(np.uint8)

# Inverted binary mask (Foreground / Background inversion)
_, binary_inv = cv2.threshold(gray_cv, threshold_val, max_val, cv2.THRESH_BINARY_INV)

plt.figure(figsize=(12, 3.5))
plt.subplot(1, 4, 1); plt.imshow(gray_cv, cmap='gray'); plt.title("Input Grayscale"); plt.axis("off")
plt.subplot(1, 4, 2); plt.imshow(binary_cv, cmap='gray'); plt.title(f"Binary (T = {threshold_val})"); plt.axis("off")
plt.subplot(1, 4, 3); plt.imshow(binary_inv, cmap='gray'); plt.title("Inverted Binary"); plt.axis("off")

# Histogram of grayscale intensities
plt.subplot(1, 4, 4)
plt.hist(gray_cv.ravel(), bins=32, range=(0, 256), color='#a855f7', alpha=0.85)
plt.axvline(threshold_val, color='#ef4444', linestyle='--', label=f'T = {threshold_val}')
plt.title("Intensity Histogram & Cutoff")
plt.xlabel("Gray Level [0..255]"); plt.ylabel("Count")
plt.legend(loc='upper right')
plt.tight_layout()
plt.show()

# ============================================================================
# 7. STUDENT PRACTICE TASKS & SOLUTIONS
# ============================================================================

# Task 1: Color Channel Isolation (Split into R, G, B)
b_ch, g_ch, r_ch = cv2.split(img_bgr)
print(f"Task 1: Mean intensities -> Red: {r_ch.mean():.1f}, Green: {g_ch.mean():.1f}, Blue: {b_ch.mean():.1f}")

# Task 2: Custom Multi-Threshold Binarization
for t in (80, 128, 180):
    bin_t = (gray_cv > t).astype(np.uint8) * 255
    white_ratio = (bin_t == 255).mean() * 100
    print(f"Task 2: Threshold T = {t:3d} ➔ White pixels = {white_ratio:.1f}%")

print("\n✓ Session 04 Python pipeline executed successfully.")
