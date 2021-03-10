import cv2

import numpy as np

# Read photo

img=cv2.imread('boy.jpg')

# Image zoom

img = cv2.resize(img,None,fx=0.5,fy=0.5)

rows,cols,channels = img.shape

print(rows,cols,channels)

cv2.imshow('img',img)

# Convert picture to grayscale

hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

cv2.imshow('hsv',hsv)

# Image binarization processing

lower_blue=np.array([90,70,70])

upper_blue=np.array([110,255,255])

mask = cv2.inRange(hsv, lower_blue, upper_blue)

#erode& dilate

erode=cv2.erode(mask,None,iterations=1)

cv2.imshow('erode',erode)

dilate=cv2.dilate(erode,None,iterations=1)

cv2.imshow('dilate',dilate)

#Traversal replacement
for i in range(rows):
  for j in range(cols):
      if dilate[i, j] == 255:
          img[i, j] = (0, 0, 255)
      # img = cv2.flip(img, 1)	#Image inversion, 1: Horizontal flipping 0: Vertical flipping -1: Horizontal and vertical flipping

  cv2.imshow('res',img)

# Window waiting command, 0 means infinite waiting

cv2.waitKey(0)
