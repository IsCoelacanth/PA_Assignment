import cv2
import numpy as np
from math import floor
def find_next(px):
    return 255 * floor(px/128)

# def sierra(img):
#     x = img.shape[0]
#     y = img.shape[1]

#     for i in range(x-2):
#         for j in range(y-2):
#             old_px = img[i][j]
#             new_px = find_next(old_px)
#             err = old_px - new_px
#             img[i][j] = new_px

#             img[i + 1][j    ] += err * 5/32
#             img[i + 2][j    ] += err * 3/32
#             img[i - 1][j + 1] += err * 4/32
#             img[i - 2][j + 1] += err * 2/32
#             img[i    ][j + 1] += err * 5/32
#             img[i + 1][j + 1] += err * 4/32
#             img[i + 2][j + 1] += err * 2/32
#             img[i    ][j + 2] += err * 3/32
#             img[i + 1][j + 2] += err * 2/32
#             img[i - 1][j + 2] += err * 2/32
#     return img

def sierra(img):
    x = img.shape[0]
    y = img.shape[1]

    for i in range(x-1):
        for j in range(y-1):
            old_px = img[i][j]
            new_px = find_next(old_px)
            err = old_px - new_px
            img[i][j] = new_px

            img[i + 1][j    ] += err * 2/4
            img[i    ][j + 1] += err * 1/4
            img[i - 1][j + 1] += err * 1/4
    return img


