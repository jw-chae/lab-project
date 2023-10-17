import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import ImageFont, ImageDraw, Image
import os
import easyocr

os.environ['KMP_DUPLICATE_LIB_OK']='True'
image = cv2.imread('./images/p1.png')
# Apply the perspective transformation

img_pers = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
reader = easyocr.Reader(['en'])
result2 =  reader.readtext(img_pers)

image_pers_result = Image.fromarray(img_pers)

# Ensure 'data' directory exists
if not os.path.exists('data'):
    os.makedirs('data')
# Ensure 'data/images' directory exists
if not os.path.exists('data/images'):
    os.makedirs('data/images')

final_boxes = []
final_texts = [] # Add this to store final text corresponding to final_boxes
count = 0
prev_box = None
prev_text = None

# Open gt.txt file in append mode
with open('data/gt.txt', 'a') as gt_file:
    print("result2 길이",len(result2))
    for bounding_boxes, text, _ in result2:
        merged_boxes = []
        merged_text = []  # Add this to store the merged text
        # Reformat bounding_boxes to have 2 points in one sublist
        bounding_boxes = [bounding_boxes[n:n+4] for n in range(0, len(bounding_boxes), 4)]
        for i in bounding_boxes:
            try:
                x1, y1 = i[0]  # the first coordinate
                x2, y2 = i[2]  # the third coordinate

                if prev_box and abs(x1 - prev_box[2]) <= 80 and abs(prev_box[2] - prev_box[0]) <= 100 and abs(x2 - x1) <= 100:
                    print("previous width랑 현재 width 가 둘 다 100 이하고 이전 x2랑 현재 x1의 차이가 100 이하인 경우")
                    prev_x1, prev_y1, prev_x2, prev_y2 = prev_box
                    merged_box = [min(x1, prev_x1), min(y1, prev_y1), max(x2, prev_x2), max(y2, prev_y2)]
                    merged_boxes.append(merged_box)

                    merged_text.append(prev_text + " " + text) # Add this line to merge the previous text with the current text

                    # Remove the previous and current box
                    if final_boxes.count(prev_box) > 0:
                        final_boxes.remove(prev_box)
                    if final_boxes.count([x1, y1, x2, y2]) > 0:
                        final_boxes.remove([x1, y1, x2, y2])

                    # Also remove the corresponding text
                    if prev_text in final_texts:
                        final_texts.remove(prev_text)

                else:
                    merged_boxes.append([x1, y1, x2, y2])
                    merged_text.append(text)

                prev_box = [x1, y1, x2, y2]
                prev_text = text

            except ValueError:
                # Skip the iteration and proceed to the next box if `i` doesn't have 4 values
                print("ValueError:", i)
                continue

        final_boxes.extend(merged_boxes)
        final_texts.extend(merged_text)  # Add this line to extend the final_texts list with merged_text

    # Draw the bounding box
    for i, (x1, y1, x2, y2) in enumerate(final_boxes):
        w = x2 - x1
        h = y2 - y1

        # Ensure the bounding box is within the image bounds
        height, width, _ = img_pers.shape
        x1, x2 = max(0, int(x1)), min(width, int(x2))
        y1, y2 = max(0, int(y1)), min(height, int(y2))

        # Ensure the bounding box is not empty
        if x1 < x2 and y1 < y2:
            img_pers = cv2.rectangle(img_pers, (x1, y1), (x2, y2), (255, 0, 0), 2)

            # Crop the image to the size of the bounding box and save it in out
            cropped_img = img_pers[y1:y2, x1:x2]
            filename = f'image_{str(count).zfill(5)}.png'
            cv2.imwrite(f'data/images/{filename}', cv2.cvtColor(cropped_img, cv2.COLOR_RGB2BGR))

            # Append to gt.txt file
            gt_file.write(f'images/{filename}\t{final_texts[i]}\n')

            count += 1
print(len(final_boxes), len(final_texts))
plt.figure(figsize=(20, 12))
plt.imshow(img_pers)
plt.show()