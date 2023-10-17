import cv2
import numpy as np

# 마우스 콜백 함수
def show_hsv(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        print("HSV Value at ({}, {}): {}".format(x, y, hsv[y, x]))

# 이미지 로드
img = cv2.imread('./images/4.jpg')

cv2.namedWindow('image')
cv2.setMouseCallback('image', show_hsv)

while True:
    cv2.imshow('image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # q키를 누르면 종료
        break

cv2.destroyAllWindows()
