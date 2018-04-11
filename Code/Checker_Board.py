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

def checkerboard_fs(img,I, J, m, n):
    # print(I, J)
    k = I; l = J
    m += I 
    n += J 
    
    while k < m and l < n :
        for i in range(l, n-1):
            pixel = img[k][i]
            new_px = apply_threshold(pixel)
            err = pixel - new_px
            err = err / 16
            img[k][i] = new_px
            if k == i :
                img[k    ][i + 1] += (err * 7)
                img[k + 1][i    ] += (err * 5)
                img[k + 1][i + 1] += (err * 1)
            if i == n - 1:
                img[k + 1][i    ] += (err * 5)
                img[k + 1][i - 1] += (err * 3)
            else :
                img[k    ][i + 1] += (err * 7)
                img[k + 1][i - 1] += (err * 3)
                img[k    ][i    ] += (err * 5)
                img[k + 1][i + 1] += (err * 1)
            # print(img[k][i], end = ' ')
        # print()
                
        k += 1

        for i in range(k, m):
            pixel = img[i][n-1]
            new_px = apply_threshold(pixel)
            err = pixel - new_px
            err = err / 16
            img[i][n-1] = new_px

            if i == k :
                img[i    ][n - 1 - 1] += (err * 7)
                img[i + 1][n - 1    ] += (err * 5)
                img[i - 1][n - 1 - 1] += (err * 1)
            elif i == m - 1:
                img[i - 1][n - 1 - 1] += (err * 1)
                img[i - 1][n - 1 - 1] += (err * 3)
            else :
                img[i + 1][n - 1    ] += (err * 7)
                img[i + 1][n - 1 - 1] += (err * 3)
                img[i    ][n - 1    ] += (err * 5)
                img[i - 1][n - 1 - 1] += (err * 1)
        
        n -= 1

        if k < m :
            for i in range(n-1, (l-1), -1):
                pixel = img[m - 1][i]
                new_px = apply_threshold(pixel)
                err = pixel - new_px
                err = err / 16
                img[m - 1][i] = new_px

                if i == k :
                    img[m - 1    ][i - 1] += (err * 7)
                    img[m - 1 - 1][i     ] += (err * 5)
                    img[m - 1 - 1][i - 1] += (err * 1)
                elif i == l:
                    img[m - 1 - 1][i     ] += (err * 1)
                    img[m - 1 - 1][i + 1] += (err * 3)
                else :
                    img[m - 1 - 1][i    ] += (err * 7)
                    img[m - 1 - 1][i + 1] += (err * 3)
                    img[m - 1    ][i - 1] += (err * 5)
                    img[m - 1 - 1][i - 1] += (err * 1)

            m -= 1
        
        if l < n :
            for i in range (m-1, k-1, -1):
                img[i][l]
                pixel = img[i][l]
                new_px = apply_threshold(pixel)
                err = pixel - new_px
                err = err / 16
                img[i][l] = new_px

                if i == m - 1 :
                    img[i    ][l + 1] += (err * 7)
                    img[i - 1][l     ] += (err * 5)
                    img[i - 1][l + 1] += (err * 1)
                elif i == l:
                    img[i + 1][l + 1] += (err * 1)
                    img[i    ][l + 1] += (err * 3)
                else :
                    img[i - 1][i    ] += (err * 7)
                    img[i - 1][i + 1] += (err * 3)
                    img[i    ][i + 1] += (err * 5)
                    img[i + 1][i + 1] += (err * 1)
            l += 1


def main():
    s_x = []
    s_y = []
    p_x = []
    p_y = []

    skl = 0.0625
    iimg = cv2.imread('../images/image.jpg', 0)
    iimg = cv2.bitwise_not(iimg)
    while ( skl <= 8):
        limg = cv2.resize(iimg, (0,0), fx= 1/skl, fy = 1/skl)
        img = cv2.resize(limg, (((limg.shape[0]//8)*8), ((limg.shape[1]//8)*8)))
        e_processes = []
        o_processes = []
        events = [th.Event()]
        events[0].clear()
        output = img.copy()
        flip = 1
        for i in range(0, img.shape[0], 8):
            for j in range(0, img.shape[1], 8):
                if flip > 0:
                    flip *= -1
                    e_processes.append(th.Thread(target=checkerboard_fs, args = (output, i, j, 8, 8)))
                else :
                    flip *= -1
                    o_processes.append(th.Thread(target=checkerboard_fs, args = (output,i ,j , 8, 8)))
        now = T.time()
        print(len(e_processes))
        for i in e_processes:
            i.start()
        for i in e_processes:
            i.join()
        for i in o_processes:
            i.start()
        for i in o_processes:
            i.join()
        p_x.append(1/skl)
        p_y.append((T.time() - now) / (len(e_processes)))
        print('Time taken parallel : {}'.format((T.time() - now) / (len(e_processes))))
        output = cv2.resize(output, (limg.shape[1], limg.shape[0]))
        cv2.imwrite('../images/doggo_chker_{}.png'.format(1/skl), cv2.bitwise_not(output))
        plt.imshow(output, cmap='Greys')
        plt.show()

        now = T.time()
        img_fs = img.copy()
        fs(img_fs)
        s_y.append(T.time() - now)
        s_x.append(1/skl)
        print('Time taken serial : {}'.format(T.time() - now))
        cv2.imwrite('../images/doggo_chker_ser_{}.png'.format(1/skl), cv2.bitwise_not(output))
        plt.imshow(img_fs, cmap='Greys')
        plt.show()
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
    plt.savefig('../images/F_S_Parr_chker_Vs_SR.png', bbox_inches='tight')
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
    plt.savefig('../images/F_S_Parr_ckher_Vs_SR_speedup.png', bbox_inches='tight')
    plt.show()

main()