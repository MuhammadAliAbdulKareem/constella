# Multimedia Systems - Session 05: Image Histogram
import cv2
import numpy as np
import matplotlib.pyplot as plt

# 1. read the image twice: gray (0) and color
gray = cv2.imread('/content/image_name.jpg', 0)
img = cv2.imread('/content/image_name.jpg')

if gray is None:
    print("Error: image not found! Check the path.")
else:
    # 2. histogram with plt.hist
    plt.hist(gray.ravel(), 256, (0, 256))
    plt.title('plt.hist')
    plt.show()

    # 3. histogram with calcHist
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    plt.plot(hist)
    plt.title('calcHist (gray)')
    plt.show()

    # 4. color histogram: B, G, R
    for i, col in enumerate(('b', 'g', 'r')):
        h = cv2.calcHist([img], [i], None, [256], [0, 256])
        plt.plot(h, color=col)
    plt.title('calcHist (color)')
    plt.show()
