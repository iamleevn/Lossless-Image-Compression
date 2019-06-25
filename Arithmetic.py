import cv2 as cv
import numpy as np
import random


class ArithmeticCoding:
    def __init__(self, size):
        self.size = size
        self.data = []
        self.freq = {}

    def make_data(self):
        data = []
        for i in range(self.size):
            i = random.randint(-1, 255)
            data.append(i)
        self.data = data
        print("Original data: ")
        print(data)

        # make frequences
        fre = {}
        for num in data:
            if not num in fre:
                fre[num] = 0
            fre[num] += 1
        self.freq = fre

        # make range_low and range_high
        low = high = 0.0
        range_low = {}
        range_high = {}
        for key in self.freq:
            high = low + self.freq[key] / self.size
            range_low[key] = low
            range_high[key] = high
            low = high

        self.range_low = range_low
        self.range_high = range_high



    def value(self, code):
        res = 0.0
        x = -1
        if not code:
            return 0.0
        for kt in code:
            res = res + int(kt) * (2 ** x)
            x -= 1
        return res

    def generate_code(self, low, high):
        code = []
        k = 0
        while (self.value(code) < low):
            code.append(1)
            if (self.value(code) > high):
                code[k] = 0
            k += 1
        temp = ""
        for kt in code:
            temp += str(kt)
        return temp

    def encode(self):
        self.make_data()

        low = old_low = 0.0
        high = 1.0
        Range = 1.0
        for num in self.data:
            low = old_low + Range * self.range_low[num]
            high = old_low + Range * self.range_high[num]
            Range = high - low
            old_low = low



        code = self.generate_code(low, high)
        print("Code: " + code)
        size_compress_file = len(code) / 8
        print("Compress ratio: " + str(self.size / size_compress_file))
        return code

    def decode(self, code):
        value = self.value(code)
        data = []
        dem = 0
        while True:
            num = 0
            for key in self.range_low:
                if self.range_low[key] <= value and value < self.range_high[key]:
                    num = key
                    break
            data.append(num)
            dem += 1
            low = self.range_low[num]
            high = self.range_high[num]
            Range = high - low
            value = (value - low) / Range
            if dem == self.size:
                break
        data = data[:self.size]
        print("Decompressed data: ")
        print(data)

"""
lee = ArithmeticCoding(14)
code = lee.encode()
lee.decode(code)
"""
