import numpy as np
import cv2
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

        res_images = []  # 각 템플릿과의 매칭 결과를 저장할 리스트

        for temp in templates:
            template = cv2.imread(temp)
            template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

            # template의 keypoints와 descriptors 계산
            kp_temp, desc_temp = sift.detectAndCompute(template_gray, None)

            # K-NN matching
            matches = flann.knnMatch(desc_img, desc_temp, k=2)

            # Lowe's ratio test
            ratio = 0.4
            good_matches = [first for first, second in matches if first.distance < ratio * second.distance]

            print(f'matches: {len(good_matches)}/{len(matches)}')

            if len(good_matches) >= 4:
                # RANSAC을 적용하여 나쁜 매칭 제거
                src_pts = np.float32([kp_img[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
                dst_pts = np.float32([kp_temp[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
                
                M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
                matchesMask = mask.ravel().tolist()
                
                draw_params = dict(matchColor = (0,255,0), 
                                   singlePointColor = None, 
                                   matchesMask = matchesMask, 
                                   flags = 2)

                res = cv2.drawMatches(img, kp_img, template, kp_temp, good_matches, None, **draw_params)
            else:
                res = cv2.drawMatches(img, kp_img, template, kp_temp, good_matches, None, 
                                      flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)

            res_images.append(res)

        return res_images


# 사용 예시
# temp_list = ['template/t5.png', 'template/t6.png','template/t7.png', 'template/t8.png']
# img_path = 'images/img_front/700.jpg'
# result_images = ImagePreprocessor.preprocess(img_path, temp_list)

temp_list = ['template/t1.png', 'template/t2.png',
             'template/t3.png', 'template/t4.png']
img_path = 'images/img_behind/701.jpg'
result_images = ImagePreprocessor.preprocess(img_path, temp_list)

# 결과 출력
for i, res in enumerate(result_images):
    cv2.imshow(f'Matching with template {i+1}', res)

cv2.waitKey(0)
cv2.destroyAllWindows()