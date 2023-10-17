import cv2
import matplotlib.pyplot as plt
import numpy as np

# 이미지 로드
img = cv2.imread('C:/Users/joong/OneDrive/Documents/code_projects/lab_project/CHAE_OCR_Final/images/img_behind/701.jpg',0)
img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)  # 색상 이미지로 변환 (사각형 그리기를 위해)

# 템플릿 로드
templates = ['template/t1.png', 'template/t2.png', 'template/t3.png', 'template/t4.png', 'template/t5.png', 'template/t6.png','template/t7.png']

# 중심점을 저장할 리스트 초기화
centers = []

for temp in templates:
    template = cv2.imread(temp,0)
    w, h = template.shape[::-1]

    # 템플릿 매칭 수행
    res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where( res >= threshold)

    # 매칭된 부분에 사각형 그리기
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_color, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

    # 매칭된 부분의 중심점 계산
    # center_x = int(np.mean(loc[1]))
    # center_y = int(np.mean(loc[0]))
    # centers.append((center_x, center_y))
    
# centers = [(x+10, y+10) for x, y in centers]
# # 네 개의 중심점을 기준으로 perspective 변환
# src_pts = np.float32(centers)
# dst_pts = np.float32([[0, img.shape[0]], [0, 0] ,[img.shape[1], 0], [img.shape[1], img.shape[0]]])

# M = cv2.getPerspectiveTransform(src_pts, dst_pts)
# img_perspective = cv2.warpPerspective(img_color, M, (img.shape[1], img.shape[0]))  # 색상 이미지에 대해 변환

# 결과 출력
plt.imshow(cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB))  # Matplotlib은 RGB 순서를 사용하므로 변환
plt.show()
