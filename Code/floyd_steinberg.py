import cv2
import numpy as np
from math import floor


def apply_threshold(value):
        return 255 * floor(value/128)

def fs(img):
    x = img.shape[0]
    y = img.shape[1]

    for i in range(x-1):
        for j in range(y-1):
            old_px = img[i][j]
            new_px = apply_threshold(old_px)
            err = old_px - new_px
            img[i][j] = new_px
            img[i + 1][j    ] += err * 7/16
            img[i - 1][j + 1] += err * 3/16
            img[i    ][j + 1] += err * 5/16
            img[i + 1][j + 1] += err * 1/16
        print(img[i][:])
    return img