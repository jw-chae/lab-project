import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('./images/p2.png', 0)
img = cv2.medianBlur(img, 5)  # Noise reduction

# Normal binary threshold
ret, th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# Adaptive mean threshold
th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 3)

# Adaptive Gaussian threshold
th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 13, 3)

# Otsu's thresholding
ret, th4 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Plotting
# titles = ['Original Image', 'Simple Thresholding (v = 127)',
#           'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding', "Otsu's Thresholding"]
# images = [img, th1, th2, th3, th4]

# # Create subplot for each image
# for i in range(5):
#     plt.subplot(3, 2, i+1), plt.imshow(images[i], 'gray')
#     plt.title(titles[i])
#     plt.xticks([]), plt.yticks([])

# # Plot histogram
# plt.subplot(3, 2, 6), plt.hist(img.ravel(), 256)
# plt.title('Histogram')
# plt.xticks([]), plt.yticks([])
plt.imshow(th3, 'gray')
plt.show()
