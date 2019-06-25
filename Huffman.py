import cv2 as cv
import numpy as np
import queue
import os


# class node
class Node:
    def __init__(self, key, freq):
        self.key = key
        self.freq = freq
        self.left = None
        self.right = None

    def __eq__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return self.freq == other.freq

    def __lt__(self, other):
        return self.freq < other.freq


# class Huffman Coding
class HuffmanCoding:
    def __init__(self, path):
        self.path = path
        self.my_queue = queue.PriorityQueue()
        self.codes = {}
        self.reverse_map = {}
        self.row = 0
        self.col = 0

    def make_data(self):
        img = cv.imread(self.path)
        # cv.imshow('Original file', img)
        blue, green, red = cv.split(img)
        self.row, self.col = blue.shape

        # merge 3 color channel array to a 1D array
        data1, data2, data3 = np.array(blue), np.array(green), np.array(red)
        data = np.concatenate((data1, data2))
        data = np.concatenate((data, data3))
        data = np.ravel(data)

        return data

    def make_frequence(self, data):
        frequence = {}
        for num in data:
            if not num in frequence:
                frequence[num] = 0
            frequence[num] += 1
        return frequence

    def make_queue(self, frequence):
        for value in frequence:
            node = Node(value, frequence[value])
            self.my_queue.put(node)

    def merge_nodes(self):
        while (self.my_queue.qsize() > 1):
            node1, node2 = self.my_queue.get(), self.my_queue.get()
            new_node = Node(None, node1.freq + node2.freq)
            new_node.left = node1
            new_node.right = node2
            self.my_queue.put(new_node)

    def make_codes_helper(self, root, curr_code):
        if root == None:
            return

        if root.key != None:
            self.codes[root.key] = curr_code
            self.reverse_map[curr_code] = root.key
            return

        self.make_codes_helper(root.left, curr_code + "0")
        self.make_codes_helper(root.right, curr_code + "1")

    def make_codes(self):
        root = self.my_queue.get()
        curr_code = ""
        self.make_codes_helper(root, curr_code)

    def get_encoded_data(self, data):
        encoded_data = ""
        for num in data:
            encoded_data += self.codes[num]
        return encoded_data

    # added padding to the encoded text, if it’s not of a length of multiple of 8
    def pad_encoded_data(self, encoded_data):
        extra_padding = 8 - len(encoded_data) % 8
        for i in range(extra_padding):
            encoded_data += "0"

        padded_info = '{0:08b}'.format(extra_padding)
        encoded_data = padded_info + encoded_data

        return encoded_data

    def get_byte_array(self, padded_encoded_data):
        b = bytearray()
        for i in range(0, len(padded_encoded_data), 8):
            byte = padded_encoded_data[i:i + 8]
            b.append(int(byte, 2))
        return b

    def compress(self, output_path):

        with open(output_path, 'wb') as output:
            data = self.make_data()
            frequence = self.make_frequence(data)
            self.make_queue(frequence)
            self.merge_nodes()
            self.make_codes()

            encoded_data = self.get_encoded_data(data)
            padded_encoded_data = self.pad_encoded_data(encoded_data)

            b = self.get_byte_array(padded_encoded_data)
            output.write(bytes(b))
        """
        # print compress's info
        print("Compressed!!!")
        # file size in bytes
        old_size = os.path.getsize(self.path)
        new_size = os.path.getsize(output_path)

        print("Before compress file's size: " + str(old_size))
        print("After compress file's size: " + str(new_size))
        print("Compress ratio: " + str(old_size / new_size))
        """

    # decompress's functions
    def remove_padding(self, padded_encoded_data):
        padded_info = padded_encoded_data[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_data = padded_encoded_data[8:]
        encoded_data = padded_encoded_data[:-1 * extra_padding]

        return encoded_data

    def decode_data(self, encoded_data):
        curr_code = ""
        decoded_data = []

        for bit in encoded_data:
            curr_code += bit
            if curr_code in self.reverse_map:
                num = self.reverse_map[curr_code]
                decoded_data.append(num)
                curr_code = ""

        return decoded_data

    def decompress(self, input_path, output_path):

        with open(input_path, 'rb') as file:
            padded_encoded_data = ""

            byte = file.read(1)
            while byte != b'':
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                padded_encoded_data += bits
                byte = file.read(1)

            encoded_data = self.remove_padding(padded_encoded_data)
            decoded_data = self.decode_data(encoded_data)

        data = np.array(decoded_data)
        data1, data2, data3 = np.split(data, 3)

        data1 = data1.reshape(self.row, self.col)
        data2 = data2.reshape(self.row, self.col)
        data3 = data3.reshape(self.row, self.col)

        decompress_image = cv.merge((data1, data2, data3))
        cv.imwrite(output_path, decompress_image)
        # cv.imshow('Decompressed Image', decompress_image)

        """
        # print decompress's info
        print("Decompressed!!!")
        origin_size = os.path.getsize(self.path)
        decompress_size = os.path.getsize(output_path)
        print("Original file's size: " + str(origin_size))
        print("Decompressed file's size: " + str(decompress_size))
        """
"""
h = HuffmanCoding('BLK.bmp')
# compress .bmp file and save to .bin file
h.compress('compress.bin')
# decompress file .bin file and save to .bmp file
h.decompress('compress.bin', 'decompressed.bmp')
"""


