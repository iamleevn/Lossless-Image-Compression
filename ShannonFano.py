import cv2 as cv
import numpy as np
from operator import itemgetter
import os


class Node:
    def __init__(self, key, freq):
        self.key = key
        self.freq = freq


class ShannonFano:
    def __init__(self, path):
        self.path = path
        self.row = 0
        self.col = 0
        self.data = []
        self.freq = {}
        self.SF_dict = {}
        self.reverse_dict = {}

    def make_data(self):
        img = cv.imread(self.path)
        # cv.imshow('Original Image: ', img)

        b, g, r = cv.split(img)
        self.row, self.col = g.shape
        b = np.array(b)
        g = np.array(g)
        r = np.array(r)
        data = np.concatenate((b, g, r))
        data = data.ravel()
        self.data = data

        freq = {}
        for num in data:
            if not num in freq:
                freq[num] = 0
            freq[num] += 1
        self.freq = freq

    def make_code(self, seq, code):
        a = {}
        b = {}

        if len(seq) == 1:
            self.SF_dict[seq.popitem()[0]] = code
            return 0

        for item in sorted(seq.items(), key=itemgetter(1), reverse=True):
            if sum(a.values()) < sum(b.values()):
                a[item[0]] = seq[item[0]]
            else:
                b[item[0]] = seq[item[0]]

        self.make_code(a, code + "0")
        self.make_code(b, code + "1")

    def encode(self, encoded_file):
        with open(encoded_file, 'wb') as file:

            # initial data
            self.make_data()
            self.make_code(self.freq, "")

            # make reverse dict
            for key in self.SF_dict:
                self.reverse_dict[self.SF_dict[key]] = key

            # get encoded data
            encoded_data = ""
            for value in self.data:
                encoded_data += self.SF_dict[value]

            # add padding to the encoded data
            pad = 8 - len(encoded_data) % 8
            for i in range(pad):
                encoded_data += "0"

            padded_info = '{0:08b}'.format(pad)
            encoded_data = padded_info + encoded_data

            # get byte array
            b = self.get_byte_array(encoded_data)

            # write file
            file.write(bytes(b))

    def get_byte_array(self, encoded_data):
        b = bytearray()
        for i in range(0, len(encoded_data), 8):
            byte = encoded_data[i:i + 8]
            b.append(int(byte, 2))
        return b

    def decode(self, encode_file, decode_file):
        encoded_data = ""

        with open(encode_file, 'rb') as file:
            byte = file.read(1)
            while byte != b'':
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                encoded_data += bits
                byte = file.read(1)

        # remove padding
        padded_info = encoded_data[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_data = encoded_data[8:]
        encoded_data = padded_encoded_data[:-1 * extra_padding]

        # get decoded_data
        code = ""
        decoded_data = []
        for bit in encoded_data:
            code += bit
            if code in self.reverse_dict:
                num = self.reverse_dict[code]
                decoded_data.append(num)
                code = ""

        data = np.array(decoded_data)
        data1, data2, data3 = np.split(data, 3)

        data1 = data1.reshape(self.row, self.col)
        data2 = data2.reshape(self.row, self.col)
        data3 = data3.reshape(self.row, self.col)

        decompress_image = cv.merge((data1, data2, data3))
        cv.imwrite(decode_file, decompress_image)
        # cv.imshow('Decompressed Image', decompress_image)

"""
lee = ShannonFano('samples/MARBLES.bmp')
lee.encode('images/nen.shannonfano')
lee.decode('images/nen.shannonfano', 'images/giainen.bmp')

old = os.path.getsize('samples/MARBLES.bmp')
new = os.path.getsize('images/nen.shannonfano')
aha = os.path.getsize('images/giainen.bmp')

print(old, new, old / new, aha)

cv.waitKey(0)
cv.destroyAllWindows()
"""