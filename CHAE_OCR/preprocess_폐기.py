import cv2
import numpy as np
import matplotlib.pyplot as plt

class ImagePreprocessor:

    @staticmethod
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
        return shadowremov
    
    @staticmethod
    def find_first_contour_pixel(image, start_ratio, direction, bottom=False):
        height, width = image.shape[:2]
        start = (int(start_ratio[0]*width), int(start_ratio[1]*height))  # Calculate start point using ratio
        x, y = start
        print("x, y: ", x, y)
        while 0 <= y < height and 0 <= x < width:
            if np.any(image[y, x] > 0):  # If pixel is part of a contour
                return x, y

            x += direction[0]
            y += direction[1]
            
        # if bottom:  # If it's the bottom corner and no contour pixel is found, return the last y pixel
        #     if 0 <= direction[0] <= 0.1 and 0.9 <= direction[1] <= 1:  # left_bottom
        #         return 0, height-1
        #     else:  # right_bottom
        #         return width-1, height-1

        return (int(start_ratio[0]*width), int(start_ratio[1]*height))  # No contour pixel found

    @staticmethod
    def process_image(img_path, left_top, right_top, left_bottom, right_bottom,threshold=127):
        # Read the image
        image = cv2.imread(img_path)

    #    # Remove shadow
    #    shadow_removed_img = ImagePreprocessor.remove_shadow(image)

    #    # Convert to grayscale
    #    gray_img = cv2.cvtColor(shadow_removed_img, cv2.COLOR_BGR2GRAY)

        # Apply dilation and erosion
        # kernel = np.ones((3,3),np.uint8)
        # dilated_img = cv2.dilate(shadow_removed_img, kernel, iterations = 1)
        # eroded_img = cv2.erode(dilated_img, kernel, iterations = 1)
        # pre_step1 = eroded_img.copy()
        # # Apply threshold
        # _, thresh_img = cv2.threshold(pre_step1, threshold, 255, cv2.THRESH_BINARY)

        # Display the result
        # cv2.imshow('Thresholded Image', thresh_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # Apply gaussian blur to image
        image = cv2.GaussianBlur(image, (5, 5), 0)

        # Apply dilation to image
        kernel = np.ones((80,80),np.uint8)
        image = cv2.dilate(image,kernel,iterations = 1)
        image = cv2.erode(image,kernel,iterations = 1)

        # Convert the image to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define lower and upper threshold values for the orange color range
        lower_orange = np.array([0, 100, 100], dtype=np.uint8)
        upper_orange = np.array([20, 255, 255], dtype=np.uint8)

        # Threshold the image to get only the orange regions
        mask = cv2.inRange(hsv, lower_orange, upper_orange)

        # Find contours in the masked image
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Create a blank canvas to draw the contours
        canvas = np.zeros_like(image)

        # Draw the contours on the canvas
        cv2.drawContours(canvas, contours, -1, (0, 255, 0), 2)

        # Convert the canvas to RGB for plotting
        canvas_rgb = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)
        # cv2.imshow("canvas", canvas_rgb)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        
# Find the first contour pixel in each corner of the canvas
        left_top = ImagePreprocessor.find_first_contour_pixel(canvas_rgb, left_top, (1, 0))  # left
        right_top = ImagePreprocessor.find_first_contour_pixel(canvas_rgb, right_top, (-1, 0))  # right
        left_bottom = ImagePreprocessor.find_first_contour_pixel(canvas_rgb, left_bottom, (0, 1),bottom=True)  # Down_left 
        right_bottom = ImagePreprocessor.find_first_contour_pixel(canvas_rgb, right_bottom, (0, 1),bottom=True)  # Down_right , 
 
        print("left top: ", left_top, "right top: ", right_top, "left bottom: ", left_bottom, "right bottom: ", right_bottom)
        # If any of the corners is None, return None
        if None in [left_top, right_top, left_bottom, right_bottom]:
            print("Failed to find contour pixel.")
            return None
        
        #image_ori = cv2.cvtColor(cv2.imread(thresh_img), cv2.COLOR_BGR2RGB)
        image_ori = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
        #pts1 = np.float32([left_top, right_top, left_bottom, right_bottom])
        pts1 = np.float32([left_top, right_top, left_bottom, right_bottom])

        # Define the destination points. They could be any points, but in this case we'll map the original points to a rectangle.
        pts2 = np.float32([[0,0], [image_ori.shape[1],0], [0,image_ori.shape[0]], [image_ori.shape[1],image_ori.shape[0]]])

        # Get the perspective transformation matrix
        matrix = cv2.getPerspectiveTransform(pts1, pts2)

        # Apply the perspective transformation
        result = cv2.warpPerspective(image_ori, matrix, (image_ori.shape[1], image_ori.shape[0])) 
        result_bgr = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
        # cv2.imshow("result", result_bgr)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return result #, left_top, right_top, left_bottom, right_bottom
        