import cv2
import numpy as np
from matplotlib import pyplot as plt

# Gamma correction
def adjust_gamma(image, gamma=1.0):
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)

# Load image
img = cv2.imread('./images/p2.png', 0)

# Apply methods
gamma_corrected = adjust_gamma(img, 1.5)
adaptive_thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
_, binary_thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
morph_close = cv2.morphologyEx(binary_thresh, cv2.MORPH_CLOSE, kernel=np.ones((5,5),np.uint8), iterations = 2)

# Display images
titles = ['Original', 'Gamma Correction', 'Adaptive Thresholding', 'Binarization and Morphology']
images = [img, gamma_corrected, adaptive_thresh, morph_close]

for i in range(4):
    plt.subplot(2, 2, i+1), plt.imshow(images[i], 'gray')
    plt.title(titles[i])
    plt.xticks([]), plt.yticks([])
plt.show()
