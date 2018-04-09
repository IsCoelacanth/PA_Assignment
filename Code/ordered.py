import numpy as np

def ordered(img, T, mode = 's'):
    avg = img.mean()
    if mode == 'p':
        for i in range(img.shape[0]):
            img[i] = 0 if img[i] < T[i % 8] else 255
    else:
        x = img.shape[0]
        y = img.shape[1]
        for i in range(x):
            for j in range(y):
                img[i][j] = 0 if img[i][j] < T[i % 8][j % 8] else 255