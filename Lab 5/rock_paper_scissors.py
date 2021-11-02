
#This example is directly copied from the Tensorflow examples provided from the Teachable Machine.

import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import cv2
import sys
import time


# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

img = None
webCam = False

cap = cv2.VideoCapture(0)
if cap is None or not cap.isOpened():
    raise("No camera")


# Load the model
model = tensorflow.keras.models.load_model('./RPS_model/keras_model.h5')

# Load Labels:
labels=[]
f = open("./RPS_model/labels.txt", "r")
for line in f.readlines():
    if(len(line)<1):
        continue
    labels.append(line.split(' ')[1].strip())

while(True):
    ret, img = cap.read()
    img_copy = img.copy()

    rows, cols, channels = img.shape
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    size = (224, 224)
    img =  cv2.resize(img, size, interpolation = cv2.INTER_AREA)
    #turn the image into a numpy array
    image_array = np.asarray(img)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)

    cv2.imshow("Rock, paper scissors", img_copy)
    cv2.waitKey(1)

    print("I think its a:",labels[np.argmax(prediction)])

cv2.imwrite('detected_out.jpg',img)
cv2.destroyAllWindows()
