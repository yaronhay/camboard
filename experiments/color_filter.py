# SRC https://www.geeksforgeeks.org/filter-color-with-opencv/

import cv2
import numpy as np

cap = cv2.VideoCapture(1)

while (1):
    _, frame = cap.read()
    # It converts the BGR color space of image to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold of blue in HSV space
    #lower = np.array([20, 100, 100])
    #upper = np.array([30, 255, 255])

    lower = np.array([35, 140, 60])
    upper = np.array([255, 255, 180])

    # preparing the mask to overlay
    mask = cv2.inRange(hsv, lower, upper)

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
    #cv2.imshow('mask', mask)
    #cv2.imshow('result', result)

    cv2.waitKey(40)

cv2.destroyAllWindows()
cap.release()
