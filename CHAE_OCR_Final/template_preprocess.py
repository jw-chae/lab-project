import cv2
import matplotlib.pyplot as plt
import numpy as np

class ImagePreprocessor:
    @staticmethod
    def preprocess(img_path, templates):
        # 이미지 로드
        img = cv2.imread(img_path, 0)
        plt.imshow(img, cmap='gray')
        # 중심점을 저장할 리스트 초기화
        centers = []

        for temp in templates:
            template = cv2.imread(temp, 0)
            w, h = template.shape[::-1]

            # 템플릿 매칭 수행
            res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.74
            loc = np.where(res >= threshold)

            # 매칭된 부분의 중심점 계산
            try:
                center_x = int(np.mean(loc[1]))
                center_y = int(np.mean(loc[0]))
                centers.append((center_x, center_y))
            except ValueError:  # 템플릿 매칭이 성공적으로 이루어지지 않은 경우
                print(f"Template matching failed with template {temp}. The original image will be returned.")
                continue

        # 네 개의 중심점에 10을 더함
        centers = [(x+10, y+10) for x, y in centers]

        # 네 개의 중심점을 기준으로 perspective 변환
        centers.sort(key = lambda x: (x[1], x[0]))  # y 좌표 기준 오름차순 정렬 (동일한 y 좌표의 경우 x 좌표로 정렬)
        src_pts = np.float32([centers[0], centers[1], centers[3], centers[2]]) # (x_min,ymin), (x_max,ymin), (x_min,ymax), (x_max,ymax)
        dst_pts = np.float32([[0, 0], [img.shape[1], 0], [0,img.shape[0]], [img.shape[1], img.shape[0]]])  # 변경된 순서에 맞춤

        M = cv2.getPerspectiveTransform(src_pts, dst_pts)
        img_perspective = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))

        #show perspective image
        plt.imshow(img, cmap='gray')
        plt.imshow(img_perspective, cmap='gray')
        return img_perspective


# 사용 예시
# temp_list = ['template/t1.png', 'template/t2.png', 'template/t3.png', 'template/t4.png','template/t5.png','template/t6.png'
#              ,'template/t7.png','template/t8.png','template/t9.png','template/t10.png','template/t11.png']
# img_path = 'images/img_front/700.jpg'
# result = ImagePreprocessor.preprocess(img_path, temp_list)
