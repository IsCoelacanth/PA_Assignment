import cv2
from PIL import Image
import PIL.ImageOps
import numpy as np
import matplotlib.pyplot as plt
from floyd_steinberg import fs
from sierra import sierra
from constant_threshold import const_thresh


def main():
    img = cv2.imread('image.jpg', 0)
    img = cv2.bitwise_not(img)
    tmp = img
    plt.imshow(img, cmap='Greys')
    plt.show()
    img_ct = const_thresh(img)
    plt.imshow(img_ct, cmap='Greys')
    plt.show()
    # img_fs = fs(img)
    # plt.imshow(img_fs, cmap='Greys')
    # plt.show()
    # img = tmp
    # img_s = sierra(img)
    # plt.imshow(img_s, cmap='Greys')
    # plt.show()
main()
