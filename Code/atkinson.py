import cv2
import numpy as np
from math import floor

def find_next(px):
    return 255 * floor(px/128)

def atkinson(img):
    x = img.shape[0]
    y = img.shape[1]
    for i in range(x-2):
        for j in range(y-2):
            old_px = img[i][j]
            new_px = find_next(old_px)
            err = old_px - new_px
            img[i][j] = new_px

            img[i    ][j + 1] += err * 1./8
            img[i    ][j + 2] += err * 1./8
            img[i + 1][j - 1] += err * 1./8
            img[i    ][j + 1] += err * 1./8
            img[i + 1][j + 1] += err * 1./8
            img[i + 2][j    ] += err * 1./8
    img[:, -1] = 1
    img[-1, :] = 1
    return img