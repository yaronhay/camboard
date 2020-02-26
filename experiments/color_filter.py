# SRC https://www.geeksforgeeks.org/filter-color-with-opencv/

import cv2
import numpy as np

cap = cv2.VideoCapture(2)

cv2.namedWindow('Colorbars')  # Create a window named 'Colorbars'


def nothing():
    pass


# assign strings for ease of coding
hh = 'Hue High'
hl = 'Hue Low'
sh = 'Saturation High'
sl = 'Saturation Low'
vh = 'Value High'
vl = 'Value Low'
wnd = 'Colorbars'
# Begin Creating trackbars for each
cv2.createTrackbar(hl, wnd, 0, 179, nothing)
cv2.createTrackbar(hh, wnd, 10, 179, nothing)
cv2.createTrackbar(sl, wnd, 178, 255, nothing)
cv2.createTrackbar(sh, wnd, 255, 255, nothing)
cv2.createTrackbar(vl, wnd, 177, 255, nothing)
cv2.createTrackbar(vh, wnd, 255, 255, nothing)

while (1):
    _, frame = cap.read()
    # It converts the BGR color space of image to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold of blue in HSV space
    # lower = np.array([35, 140, 60])
    # upper = np.array([255, 255, 180])

    # lower = np.array([0, 0, 30])
    # upper = np.array([80, 80, 255])

    hul = cv2.getTrackbarPos(hl, wnd)
    huh = cv2.getTrackbarPos(hh, wnd)
    sal = cv2.getTrackbarPos(sl, wnd)
    sah = cv2.getTrackbarPos(sh, wnd)
    val = cv2.getTrackbarPos(vl, wnd)
    vah = cv2.getTrackbarPos(vh, wnd)

    # make array for final values
    HSVLOW = np.array([hul, sal, val])
    HSVHIGH = np.array([huh, sah, vah])

    l1 = np.array([0, 70, 50])
    u1 = np.array([10, 255, 255])

    l2 = np.array([170, 70, 50])
    u2 = np.array([180, 255, 255])

    # preparing the mask to overlay
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    mask1 = cv2.inRange(hsv, l1, u1)
    mask2 = cv2.inRange(hsv, l1, u1)

    #mask = cv2.bitwise_or(mask1, mask2)
    mask = cv2.inRange(hsv, HSVLOW, HSVHIGH)

    # The black region in the mask has the value of 0,
    # so when multiplied with original image removes all non-blue regions
    result = cv2.bitwise_and(frame, frame, mask=mask)
    try:
        M = cv2.moments(mask)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
        cv2.putText(frame, "centroid", (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    except ZeroDivisionError:
        pass
    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    # cv2.imshow('result', result)

    cv2.waitKey(40)

cv2.destroyAllWindows()
cap.release()
