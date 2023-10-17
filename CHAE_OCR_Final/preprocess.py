import cv2
import numpy as np
import matplotlib.pyplot as plt
class ImagePreprocessor:
    @staticmethod
    def preprocess(img_path, templates):
        # 이미지 로드
        img = cv2.imread(img_path)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # SIFT 생성
        sift = cv2.xfeatures2d.SIFT_create()

        # img의 keypoints와 descriptors 계산
        kp_img, desc_img = sift.detectAndCompute(img_gray, None)

        # FLANN matcher 설정
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)

        centers = []  # 각 템플릿의 매칭된 좌표들의 중심점을 저장할 리스트

        for temp in templates:
            template = cv2.imread(temp)
            template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

            # template의 keypoints와 descriptors 계산
            kp_temp, desc_temp = sift.detectAndCompute(template_gray, None)

            # K-NN matching
            matches = flann.knnMatch(desc_img, desc_temp, k=2)

            # Lowe's ratio test
            ratio = 0.45
            good_matches = [first for first, second in matches if first.distance < ratio * second.distance]

            print(f'matches: {len(good_matches)}/{len(matches)}')

            if len(good_matches) >= 4:
                # RANSAC을 적용하여 나쁜 매칭 제거
                src_pts = np.float32([kp_img[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
                dst_pts = np.float32([kp_temp[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
                
                M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
                matchesMask = mask.ravel().tolist()

                # RANSAC 적용 후의 좋은 매칭들
                good_matches_after_ransac = [m for m, mask in zip(good_matches, matchesMask) if mask]

                # 좋은 매칭들의 좌표
                src_pts_after_ransac = np.float32([kp_img[m.queryIdx].pt for m in good_matches_after_ransac]).reshape(-1, 1, 2)

                # 좌표의 평균으로 중심점 계산
                center_x = np.mean(src_pts_after_ransac[:,0,0])
                center_y = np.mean(src_pts_after_ransac[:,0,1])

                # 중심점들에서 평균과의 차이가 200 이상인 점 제거
                good_centers = [(x, y) for x, y in zip(src_pts_after_ransac[:,0,0], src_pts_after_ransac[:,0,1]) 
                                if abs(x - center_x) < 100 and abs(y - center_y) < 100]

                # 제거한 후의 중심점들로 다시 평균 계산
                if good_centers:
                    center_x = np.mean([x+10 for x, y in good_centers])
                    center_y = np.mean([y+10 for x, y in good_centers])

                centers.append((center_x, center_y))
            else:
                src_pts = np.float32([kp_img[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
                center_x = np.mean(src_pts[:,0,0])
                center_y = np.mean(src_pts[:,0,1])
                centers.append((center_x, center_y))
        # 네 개의 중심점에 10을 더함
        #centers = [(int(x), int(y)) for x, y in centers]

        # 네 개의 중심점을 기준으로 perspective 변환
#        centers.sort(key = lambda x: (x[1], x[0]))  # y 좌표 기준 오름차순 정렬 (동일한 y 좌표의 경우 x 좌표로 정렬)
        src_pts = np.float32([centers[0], centers[1], centers[2], centers[3]]) # (x_min,ymin), (x_max,ymin), (x_min,ymax), (x_max,ymax)
        dst_pts = np.float32([[0, img.shape[0]],[0, 0], [img.shape[1],0], [img.shape[1], img.shape[0]]])  # 변경된 순서에 맞춤

        M = cv2.getPerspectiveTransform(src_pts, dst_pts)
        img_perspective = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))
        
        return img_perspective



# # 사용 예시


temp_list = ['template/t5.png', 'template/t6.png',
             'template/t7.png', 'template/t8.png']
img_path = 'images/img_front/700.jpg'
result_images = ImagePreprocessor.preprocess(img_path, temp_list)


# temp_list = ['template/t1.png', 'template/t2.png',
#              'template/t3.png', 'template/t4.png']
# img_path = 'images/img_front/700.jpg'
# result_images = ImagePreprocessor.preprocess(img_path, temp_list)

plt.imshow(result_images)
plt.show()