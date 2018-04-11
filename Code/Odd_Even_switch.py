import cv2
import numpy as np
import matplotlib.pyplot as plt
from floyd_steinberg import fs
from atkinson import atkinson
from sierra import sierra
from Stucki import stucki
import threading as th
import time as T
from utils import scaler

def main():
    s_x = []
    s_y = []
    p_x = []
    p_y = []

    skl = 0.125
    iimg = cv2.imread('../images/image.jpg', 0)
    iimg = cv2.bitwise_not(iimg)
    while ( skl <= 8):
        img = cv2.resize(iimg, (0,0), fx= 1/skl, fy = 1/skl)
        o_processes = []
        e_processes = []
        output = img.copy()
        for i in range(0, output.shape[0]-2):
            if i % 2 == 0:
                e_processes.append(th.Thread(target=fs, args = (output, i, 'p',)))
            else:
                o_processes.append(th.Thread(target=fs, args = (output, i, 'p',)))
                
        now = T.time()
        for i in processes:
            i.start()
        for i in processes:
            i.join()
        p_x.append(1/skl)
        p_y.append((T.time() - now) / (len(processes)))
        print('Time taken parallel : {}'.format((T.time() - now) / (len(processes))))
        # cv2.imwrite('../images/doggo_parallel_locks.png', cv2.bitwise_not(output))
        # plt.imshow(output, cmap='Greys')
        # plt.show()

        now = T.time()
        img_fs = img.copy()
        fs(img_fs)
        s_y.append(T.time() - now)
        s_x.append(1/skl)
        print('Time taken serial : {}'.format(T.time() - now))
        # cv2.imwrite('../images/doggo_ser.png', cv2.bitwise_not(output))
        # plt.imshow(img_fs, cmap='Greys')
        # plt.show()
        skl *= 2

    # s_y_ = scaler(s_y.copy())
    # p_y_ = scaler(p_y.copy())
    plt.figure()
    plt.plot(s_x, s_y, color='red', label='Serial')
    plt.plot(p_x, p_y, color='blue', label='Parallel')
    plt.xlabel('Input size scaling factor')
    plt.ylabel('Time')
    # plt.xscale('log', basex=2)
    plt.yscale('log', basey=10)
    plt.title("Parallel vs Serial Floyd-Steinberg algorithm input image = {}X{}".format(iimg.shape[0], iimg.shape[1]))
    plt.legend()
    plt.savefig('../images/F_S_Parr_Vs_SR.png', bbox_inches='tight')
    plt.show()

    speed_up = []
    for i in range(len(s_x)):
        speed_up.append(s_y[i]/p_y[i])
    plt.plot(s_x, speed_up, label='Speed up')
    plt.xlabel('Input size 10^5')
    plt.ylabel('Time')
    plt.xscale('log', basex=2)
    plt.title("Speed up observed")
    plt.legend()
    plt.savefig('../images/F_S_Parr_Vs_SR_speedup.png', bbox_inches='tight')
    plt.show()

main()