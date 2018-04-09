import threading as th
import cv2
import matplotlib.pyplot as plt
from ordered import ordered
import time

def main():
    img = cv2.imread('image.jpg', 0)
    img = cv2.bitwise_not(img)
    T = [[ 0, 32,  8, 40,  2, 34, 10, 42],   
    [48, 16, 56, 24, 50, 18, 58, 26],   
    [12, 44,  4, 36, 14, 46,  6, 38],   
    [60, 28, 52, 20, 62, 30, 54, 22],   
    [ 3, 35, 11, 43,  1, 33,  9, 41],   
    [51, 19, 59, 27, 49, 17, 57, 25],
    [15, 47,  7, 39, 13, 45,  5, 37],
    [63, 31, 55, 23, 61, 29, 53, 21] ];
    for i in range(8):
        for j in range(8):
            T[i][j] = (T[i][j] / 64) * 255
    s_x = []
    s_y = []
    p_x = []
    p_y = []

    i = 0.25 

    while ( i <= 16):
        s_im = cv2.resize(img, (0,0), fx= 1/i, fy = 1/i)
        now = time.time()
        ordered(s_im, T)
        en = time.time()
        s_x.append(i)
        s_y.append(en-now)
        i *= 2
        if i == 2:
            plt.imshow(s_im, cmap='binary')
            plt.show()
    # print(s_x)
    # print(s_y)

    i = 0.25
    while(i <= 16):
        s_im = cv2.resize(img, (0,0), fx= 1/i, fy = 1/i)
        jobs = []
        for j in range(s_im.shape[0]):
            jobs.append(th.Thread(target=ordered, args=(s_im[j][:],T[j % 8][:],'p',)))
        now = time.time()
        for j in jobs:
            j.start()
        en = time.time()
        for j in jobs:
            j.join()
        p_x.append(i)
        p_y.append((en-now)/(len(jobs)))
        i *= 2
        if i == 2:
            plt.imshow(s_im, cmap='binary')
            plt.show()

    plt.figure()
    plt.plot(s_x, s_y, color='red', label='Serial')
    plt.plot(p_x, p_y, color='blue', label='Parallel')
    plt.xlabel('Input size')
    plt.ylabel('Time')
    plt.title("Parallel vs Serial Ordered Dither algorithm")
    plt.legend()
    plt.show()

    speed_up = []
    for i in range(len(s_x)):
        speed_up.append(s_y[i]/p_y[i])
    plt.plot(s_x, speed_up, label='Speed up')
    plt.xlabel('Input size')
    plt.ylabel('Time')
    plt.title("Speed up observed")
    plt.legend()
    plt.show()

        

main()
