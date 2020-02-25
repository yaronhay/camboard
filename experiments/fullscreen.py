import os

import cv2
import numpy as np


def show_full_screen_image():
    # os.system("screencapture screen.png")
    # img = cv2.imread('screen.png')
    img = np.zeros((720, 1280, 3), np.uint8)
    cv2.rectangle(img, (0, 0), (1275, 715), (0xff, 0, 0))
    cv2.namedWindow("test", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("test", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    while True:
        # img = np.zeros((1440,2560,3), np.uint8)
        # Note: 900x1440 is the resolution with my MBP
        # img = cv2.resize(img, (1440, 900), interpolation=cv2.INTER_CUBIC)

        cv2.imshow("test", img)
        key = cv2.waitKey(0)
        if key == ord('q'):  # ESC to exit
            break


if __name__ == '__main__':
    show_full_screen_image()
