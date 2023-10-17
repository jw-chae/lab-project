import cv2
import pandas as pd
import numpy as np
from paddleocr import PaddleOCR
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

# Setup model
ocr_model = PaddleOCR(lang='en')

def process_image(img_path, x_grid, y_grid):
    # Run the ocr method on the ocr model
    result = ocr_model.ocr(img_path)
    
    # Get all box coordinates
    all_coords = np.vstack([res[0] for res in result[0]])

    # Find min and max x and y coordinates
    x_min, y_min = np.min(all_coords, axis=0)
    x_max, y_max = np.max(all_coords, axis=0)

    # Calculate dimensions of the rectangle
    height = y_max - y_min
    width = x_max - x_min

    # Define grid size
    x_step = width // x_grid
    y_step = height // y_grid

    # Initialize grid list
    grid_list = [[None for _ in range(x_grid)] for _ in range(y_grid)]

    # Calculate center of each detected text box and assign it to the corresponding grid
    for i, res in enumerate(result[0]):
        box = res[0]
        text = res[1][0]

        # Compute center of box
        center_x = int(np.mean([point[0] for point in box]))
        center_y = int(np.mean([point[1] for point in box]))

        # Adjust the center coordinates based on the top-left corner of the rectangle
        center_x -= x_min
        center_y -= y_min

        grid_x = int(center_x // x_step)
        grid_y = int(center_y // y_step)

        # Save the text only
        grid_list[grid_y][grid_x] = text
        
    return grid_list

# Read image_Front
img_front = process_image('./images/p2.png', x_grid=8, y_grid=16)

# Select the first (y_grid - 1) rows
img_front = img_front[0:16-1]

# Read image_behind
img_behind = process_image('./images/p2.png', x_grid=8, y_grid=16)

# Select rows from (y_grid - 15) to the end
img_behind = img_behind[16-15:]

# Combine the results
combined_img = img_front + img_behind

# Convert list to pandas dataframe
df = pd.DataFrame(combined_img)

# Write to CSV file
df.to_csv('ocr_output_combined.csv', index=False, header=False)
