import cv2
import numpy as np

def increase_brightness(image, value=10):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = np.where((255 - v) < value, 255, v+value)
    final_hsv = cv2.merge((h, s, v))
    return cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

def map_colors(colors):
    result_dict = {
        'URO': colors[0],
        'BIL': colors[1],
        'KET': colors[2],
        'BLD': colors[3],
        'PRO': colors[4],
        'NIT': colors[5],
        'LEU': colors[6],
        'GLU': colors[7],
        'SG': colors[8],
        'PH': colors[9],
    }
    return result_dict

def analyze_urine_strip(image_path):
    image = cv2.imread(image_path)
    brightened_image = increase_brightness(image)
    strip_height, strip_width, _ = brightened_image.shape
    num_boxes = 10
    box_height = strip_height
    box_width = strip_width // num_boxes
    
    colors = []
    for i in range(num_boxes):
        x1 = i * box_width
        y1 = 0
        x2 = (i + 1) * box_width
        y2 = strip_height
        roi = brightened_image[y1:y2, x1:x2]
        avg_color = np.mean(roi, axis=(0, 1))
        avg_color = np.round(avg_color).astype(int)
        colors.append(avg_color)
        
    
    return map_colors(colors)

# image_path = '/content/image1.jpg'
# colors = analyze_urine_strip(image_path)

# # Print RGB values for each box
# for i, color in enumerate(colors):
#     print(f'Box {i+1}: RGB({color[2]}, {color[1]}, {color[0]})')
