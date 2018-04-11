import cv2
import numpy as np
from math import floor
from time import sleep
import threading as th
def apply_threshold(value):
        return 255 * floor(value/128)

def fs(img, lin = None, mode = 's', event=None):
    x = img.shape[0]
    y = img.shape[1]
    if mode == 'p':
        # print(event)
        if lin > 0:
            event[lin].wait()
        # print ("Process {} started".format(lin))
        # lck = th.Lock()
        # lck.acquire()
        for j in range (y - 1):
            if j == 3:
                if lin == 0 :
                    event[1].set()
                else:
                    # print ('set event ',lin)
                    if lin + 1 < x - 2:
                        event[lin+1].set()
            old_px = img[lin][j]
            new_px = apply_threshold(old_px)
            err = old_px - new_px
            err = err / 16
            img[lin][j] = new_px
            img[lin    ][j + 1] += (err * 7)
            img[lin + 1][j - 1] += (err * 3)
            img[lin    ][j    ] += (err * 5)
            img[lin + 1][j + 1] += (err * 1)
        # lck.release()
    else :      
        for i in range(x-1):
            for j in range(y-1):
                old_px = img[i][j]
                new_px = apply_threshold(old_px)
                err = old_px - new_px
                err = err / 16
                img[i][j] = new_px
                img[i    ][j + 1] += (err * 7)
                img[i + 1][j - 1] += (err * 3)
                img[i    ][j    ] += (err * 5)
                img[i + 1][j + 1] += (err * 1)
        # print(img[i][:])
    # img[:, -1] = 1
    # img[-1, :] = 1