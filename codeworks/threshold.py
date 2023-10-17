import numpy as np
import cv2
print(cv2.__version__)

# 그림자 제거 함수
def remove_shadow(img):
    rgb_planes = cv2.split(img)
    
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        result_norm_planes.append(norm_img)
        
    shadowremov = cv2.merge(result_norm_planes)
    shadowremov = cv2.erode(shadowremov, np.ones((2,2), np.uint8), iterations=1)
    
    return shadowremov

# 트랙바의 이벤트 함수
def onChange(x):
    _, th_img = cv2.threshold(remove_shadow_img_gray, x, 255, cv2.THRESH_BINARY)
    cv2.imshow('Threshold', th_img)

# 마우스 클릭 이벤트 함수
def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # 이미지의 해당 좌표에서 픽셀 값을 가져옴
        pixel = remove_shadow_img[y, x]
        # 픽셀값을 트랙바의 위치로 설정
        cv2.setTrackbarPos('Threshold', 'Threshold', pixel)

# 이미지 로드
img = cv2.imread('./images/img6.jpg')
#resize 1920x1080
img = cv2.resize(img, (1920, 1080))

# 그림자 제거
remove_shadow_img = remove_shadow(img)
remove_shadow_img_gray = cv2.cvtColor(remove_shadow_img, cv2.COLOR_BGR2GRAY)
cv2.namedWindow('Threshold')
# 트랙바 생성
cv2.createTrackbar('Threshold', 'Threshold', 0, 255, onChange)
# 마우스 클릭 이벤트 연결
cv2.setMouseCallback('Threshold', onMouse)

cv2.imshow('Original', img)
cv2.imshow('Shadow removed', remove_shadow_img)

cv2.waitKey(0)
cv2.destroyAllWindows()
