import os
import shutil
import xml.etree.ElementTree as ET
from collections import defaultdict

def get_info_from_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    size = root.find('size')
    width = int(size.find('width').text)
    height = int(size.find('height').text)
    
    boxes = []
    for obj in root.iter('object'):
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        boxes.append(b)
        
    return width, height, boxes

def convert_to_yolo_label(cls, box_info, width, height):
    x_center = (box_info[0] + box_info[1]) / 2.0
    y_center = (box_info[2] + box_info[3]) / 2.0
    w = box_info[1] - box_info[0]
    h = box_info[3] - box_info[2]
    
    # normalize
    x_center /= width
    w /= width
    y_center /= height
    h /= height
    
    return f"{cls} {x_center} {y_center} {w} {h}"

def create_directory(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

input_dir = 'input'
create_directory('images')
create_directory('labels')

# 파일을 읽는 순서대로 숫자를 할당
files = []
for filename in os.listdir(input_dir):
    if filename.endswith('.jpg') or filename.endswith('.xml'):
        files.append(filename)

# 짝수 인덱스: 이미지, 홀수 인덱스: 라벨
for i in range(0, len(files), 2):
    img_file = files[i]
    xml_file = files[i+1]

    # 이미지 파일 복사
    shutil.copy(os.path.join(input_dir, img_file), os.path.join('images', f"img{i//2+1}.jpg"))
    
    # 라벨 파일 처리
    width, height, boxes = get_info_from_xml(os.path.join(input_dir, xml_file))
    
    with open(os.path.join('labels', f"img{i//2+1}.txt"), 'w') as f:
        for box in boxes:
            label_line = convert_to_yolo_label(0, box, width, height)
            f.write(label_line + "\n")
