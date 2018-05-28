import cv2
import numpy as np
import matplotlib.pyplot as plt
from floyd_steinberg import fs
from atkinson import atkinson
from sierra import sierra
from Stucki import stucki
import threading as th
import time as T
from math import floor

def apply_threshold(value):
        return 255 * floor(value/128)

def blocked_fs(img, evt):
    if evt.is_set() == False:
        evt.wait()
    avg_1 = np.mean(img[0])
    avg_2 = np.mean(img[-1])
    for i in range(0, img.shape[0]-1):
        for j in range(img.shape[1] - 1):
            old_px = img[i][j]
            new_px = apply_threshold(old_px)
            err = old_px - new_px
            err = err / 16
            img[i][j] = new_px
            img[i    ][j + 1] += (err * 7)
            img[i + 1][j - 1] += (err * 3)
            img[i    ][j    ] += (err * 5)
            img[i + 1][j + 1] += (err * 1)

def main():
    
    s_x = []
    s_y = []
    p_x = []
    p_y = []

    skl = 1
    iimg = cv2.imread('../images/image.jpg', 0)
    iimg = cv2.bitwise_not(iimg)

    while ( skl <= 16):
        
        img = cv2.resize(iimg, None, fx= 1/skl, fy = 1/skl)
        processes = []
        event = th.Event()
        event.clear()
        output = img.copy()
        step = img.shape[0] // 16
        for i in range(0, output.shape[0]-1, step):
            processes.append(th.Thread(target=blocked_fs, args = (output[i : i+step+1], event)))

        for i in processes:
            i.start()
        
        now = T.time()
        event.set()
        for i in processes:
            i.join()
        p_x.append(1/skl)
        p_y.append((T.time() - now) / (len(processes)))
        print('Time taken parallel : {}'.format((T.time() - now) / (len(processes))))
        # if skl == 1:
        cv2.imwrite('../images/doggo_parallel_with_16_procs.png', cv2.bitwise_not(output))
        plt.imshow(output, cmap='Greys')
        plt.show()

        now = T.time()
        img_fs = img.copy()
        fs(img_fs)
        s_y.append(T.time() - now)
        s_x.append(1/skl)
        print('Time taken serial : {}'.format(T.time() - now))
        # if skl == 1:
        #     cv2.imwrite('../images/doggo_ser_1_proc.png', cv2.bitwise_not(output))
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
    plt.savefig('../images/W_16_F_S_Parr_Vs_SR.png', bbox_inches='tight')
    plt.show()

    speed_up = []
    for i in range(len(s_x)):
        speed_up.append(s_y[i]/p_y[i]*(iimg.shape[0]*s_x[i]))
    plt.plot(s_x, speed_up, label='Speed up')
    plt.xlabel('Input size 10^5')
    plt.ylabel('Time')
    plt.xscale('log', basex=2)
    plt.title("Speed up observed")
    plt.legend()
    plt.savefig('../images/W_16_F_S_Parr_Vs_SR_speedup.png', bbox_inches='tight')
    plt.show()

main()