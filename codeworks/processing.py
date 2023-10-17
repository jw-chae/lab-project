import cv2
import numpy as np

# 이미지를 불러옵니다.
image = cv2.imread('images/1.jpg')

# 이미지를 그레이스케일로 변환합니다.
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Gaussian blur를 적용하여 노이즈를 줄입니다.
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Canny edge detection을 적용합니다.
edges = cv2.Canny(blurred, 50, 150)

# 결과 이미지를 저장합니다.
cv2.imshow('Canny Edges', edges)
cv2.waitKey(0)
cv2.destroysAllWindows()