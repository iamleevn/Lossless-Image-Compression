import cv2 as cv
import ShannonFano
import Huffman
import time
import os

"""
start_sf = time.time()
# Shannon-Fano
sf = ShannonFano.ShannonFano('samples/sontung.bmp')
sf.encode('encode/sontung.sf')
sf.decode('encode/sontung.sf', 'decode/mtp.bmp')
end_sf = time.time()

start_hc = time.time()
# Huffman Coding
hc = Huffman.HuffmanCoding('samples/sontung.bmp')
hc.compress('encode/sontung.hc')
hc.decompress('encode/sontung.hc', 'decode/mtp.bmp')
end_hc = time.time()

print('Shannon Fano\'s runtime: %f ms' %((end_sf - start_sf) * 1000))
print('Huffman Coding\'s run    time: %f ms ' % ((end_hc - start_hc) * 1000))
"""

filename = ["XING_T24.TIF", "BLK.bmp"]

for i in filename:
    name = "samples/" + i

    # Shannon Fano
    sf = ShannonFano.ShannonFano(name)
    encode_file_name_sf = 'encode/' + i + '.sf'

    start_sf = time.time()
    sf.encode(encode_file_name_sf)
    end_sf = time.time()
    run_time_sf = (end_sf - start_sf)

    before_size = os.path.getsize(name)
    after_size_sf = os.path.getsize(encode_file_name_sf)
    compression_ratio_sf = before_size / after_size_sf

    # Huffman Coding
    hc = Huffman.HuffmanCoding(name)
    encode_file_name_hc = 'encode/' + i + '.hc'

    start_hc = time.time()
    hc.compress(encode_file_name_hc)
    end_hc = time.time()
    run_time_hc = end_hc - start_hc

    after_size_hc = os.path.getsize(encode_file_name_hc)
    compression_ratio_hc = before_size / after_size_hc

    print("Shannon-Fano: ", i, sf.row, 'x', sf.col, compression_ratio_sf, run_time_sf, 's')
    print("Huffman Coding: ", i, hc.row, 'x', hc.col, compression_ratio_hc, run_time_hc, 's')

cv.waitKey(0)
cv.destroyAllWindows()