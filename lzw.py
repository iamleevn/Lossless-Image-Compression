import cv2 as cv
import numpy as np
import struct
import os

# load image
img = cv.imread('samples\sontung.bmp')
# cv.imshow('image', img)
row, col, dim = img.shape

# make data from image
blue, green, red = cv.split(img)
blue = np.array(blue)
green = np.array(green)
red = np.array(red)
data = np.concatenate((blue, green, red))
# convert to 1-d array
data = data.ravel()
data_size = len(data)
# convert data to text string
text = str(data[0])
for i in range(1, data_size):
    text = text + '-' + str(data[i])

# initial dictionary
dict = {chr(i): i for i in range(256)}
dict_size = 256

# compression
compress_data = []
s = ""
for c in text:
    temp = s + c
    if temp in dict:
        s = temp
    else:
        compress_data.append(dict[s])
        dict[s] = dict_size
        dict_size += 1
        s = c
if s:
    compress_data.append((dict[s]))

# writing to binary file
out = open("adt.lzw", "wb")
for data in compress_data:
    out.write(struct.pack('i', data))
out.close()

"""

# print size of files
original_size = os.path.getsize("samples\kha.bmp")
compress_size = os.path.getsize('adt.lzw')
compress_ratio = original_size / compress_size
print("Original file's size: " + str(original_size) + " bytes")
print("Compressed file's size: " + str(compress_size) + " bytes")
print("Compress ratio: " + str(compress_ratio))

text_size = os.path.getsize('text.txt')
print(text_size)

"""
cv.waitKey(0)
cv.destroyAllWindows()
