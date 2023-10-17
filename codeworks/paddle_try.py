# Importing required functions for inference and visualization.
import paddleocr #import draw_ocr
import os
import cv2
import matplotlib.pyplot as plt
#%matplotlib inline
ocr = paddleocr.PaddleOCR(use_angle_cls=True)

def save_ocr(img_path, out_path, result, font):
  save_path = os.path.join(out_path, img_path.split('/')[-1] + 'output')
 
  image = cv2.imread(img_path)
 
  boxes = [line[0] for line in result]
  txts = [line[1][0] for line in result]
  scores = [line[1][1] for line in result]
 
  im_show = paddleocr.draw_ocr(image, boxes, txts, scores, font_path=font)
  
  cv2.imwrite(save_path, im_show)
 
  img = cv2.cvtColor(im_show, cv2.COLOR_BGR2RGB)
  plt.imshow(img)

out_path = './output_images'
font = './simfang.ttf'
img_path = './data/images/1.jpg'
result = ocr.ocr(img_path)
