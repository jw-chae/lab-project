import cv2
import numpy as np

# 마우스 콜백 함수
def draw_circle(event, x, y, flags, param):
    global mouseX, mouseY, mouseClick
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x, y), 5, (255, 0, 0), -1)
        mouseX, mouseY = x, y
        mouseClick.append((x, y))

# 원본 이미지
img = cv2.imread('./images/4.jpg')
rows, cols, ch = img.shape
# 클릭 좌표를 저장하기 위한 리스트
mouseClick = []

# 출력 이미지를 위한 캔버스
output = np.zeros((rows, cols, ch), dtype=np.uint8)

cv2.setMouseCallback('image', draw_circle)

while True:
    cv2.imshow('image', img)
    if len(mouseClick) == 3:
        pts1 = np.float32(mouseClick)
        pts2 = np.float32([[10, 10], [cols - 10, 10], [10, rows - 10]])
        # Affine Transform Matrix 계산
        M = cv2.getAffineTransform(pts1, pts2)
        # Affine Transform 적용
        output = cv2.warpAffine(img, M, (cols, rows))
        cv2.imshow('output', output)
        mouseClick = []
    if cv2.waitKey(20) & 0xFF == 27:  # ESC 키를 누르면 종료
        break

cv2.destroyAllWindows()
