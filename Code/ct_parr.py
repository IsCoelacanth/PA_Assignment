import threading as th
import cv2
import matplotlib.pyplot as plt
from constant_threshold import const_thresh
import time

def main():
    img = cv2.imread('image.jpg', 0)
    img = cv2.bitwise_not(img)

    s_x = []
    s_y = []
    p_x = []
    p_y = []

    i = 0.25 

    while ( i <= 16):
        s_im = cv2.resize(img, (0,0), fx= 1/i, fy = 1/i)
        now = time.time()
        const_thresh(s_im)
        en = time.time()
        s_x.append(i)
        s_y.append(en-now)
        i *= 2
    # print(s_x)
    # print(s_y)

    i = 0.25
    while(i <= 16):
        s_im = cv2.resize(img, (0,0), fx= 1/i, fy = 1/i)
        jobs = []
        for j in range(s_im.shape[0]):
            jobs.append(th.Thread(target=const_thresh, args=(s_im[j][:],'p',)))
        now = time.time()
        for j in jobs:
            j.start()
        for j in jobs:
            j.join()
        en = time.time()
        p_x.append(i)
        p_y.append((en-now)/(len(jobs))) # / len(jobs) because jobs are started linearly, this can be improved using map-reduce
        i *= 2
        if i == 1:
            plt.imshow(s_im, cmap='binary')
            plt.show()

    plt.figure()
    plt.plot(s_x, s_y, color='red', label='Serial')
    plt.plot(p_x, p_y, color='blue', label='Parallel')
    plt.xlabel('Input size')
    plt.ylabel('Time')
    plt.title("Parallel vs Serial Constant threshold algorithm")
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
