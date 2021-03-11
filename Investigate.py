"""
Created on Wed Mar, 3, 2021
@author: Nhu Nhat Anh

Deploy Demo
"""
import cv2
import os

from Predict import Predict

"""
Crop Square Region in image given onclick event at coordinate (x,y)
:param: src - source to the image
:param: x, y - onclick coordinates
"""
def classify_patch(src, x, y):
    # Patch retrieval
    image = cv2.imread(src)
    patch = image[y-55:y+56, x-55:x+56]
    patch_PIL = cv2.cvtColor(patch, cv2.COLOR_BGR2RGB)

    # Classification
    predicted_class = Predict(img=patch_PIL)

    # Bounding box and Class
    if predicted_class == "Normal":
        cv2.circle(image, (x,y), radius=2, color=(0,255,0), thickness=1)
        cv2.rectangle(image, (x-55, y-55), (x+55, y+55), color = (0,255,0), thickness = 2)
        cv2.putText(image, predicted_class, (x-55, y-60), fontFace = cv2.FONT_HERSHEY_PLAIN, fontScale = 1.2, color = (0,255,0), thickness = 2)
    else:
        cv2.circle(image, (x,y), radius=2, color=(0,0,255), thickness=1)
        cv2.rectangle(image, (x-55, y-55), (x+55, y+55), color = (0,0,255), thickness = 2)
        cv2.putText(image, predicted_class, (x-55, y-60), fontFace = cv2.FONT_HERSHEY_PLAIN, fontScale = 1.2, color = (0,0,255), thickness = 2)

    return image
