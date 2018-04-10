import cv2
from PIL import Image
import PIL.ImageOps
import numpy as np
import matplotlib.pyplot as plt
from floyd_steinberg import fs
from atkinson import atkinson
from sierra import sierra
from Stucki import stucki
from constant_threshold import const_thresh


def main():
    img = cv2.imread('../images/image_car.jpg', 0)
    img = cv2.bitwise_not(img)
    # img = cv2.resize(img, (0,0), fx= 2, fy = 2)
    tmp = img
    plt.imshow(img, cmap='Greys')
    plt.show()
    img_fs = fs(img.copy())
    plt.imshow(img_fs, cmap='Greys')
    plt.show()
    # img_a = atkinson(img.copy())
    # plt.imshow(img_a, cmap='Greys')
    # plt.show()
    # img_s = sierra(img.copy())
    # plt.imshow(img_s, cmap='Greys')
    # plt.show()
    img_st = stucki(img.copy())
    plt.imshow(img_st, cmap='Greys')
    plt.show()
main()
