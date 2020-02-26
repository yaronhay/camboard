import cv2
import numpy as np

##
# Color limits: tuples of lower, upper in HSV
##
BLUE_LIM = np.array([35, 140, 60]), np.array([255, 255, 180])
RED_LIM = np.array([0, 178, 177]), np.array([10, 255, 255])


def mask_by_color(frame, color_limits):
    lower, upper = color_limits
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    return mask


def estimate_location(mask):

    try:
        M = cv2.moments(mask)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        # print(cX, cY, mask.shape)
        return True, (cX, cY)
    except ZeroDivisionError:
        return False, None


def detect_object_location(frame, color_limits):
    mask = mask_by_color(frame, color_limits)
    return estimate_location(mask)


def detect_object_presence(frame, color_limits, thresh):
    mask = mask_by_color(frame, color_limits)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filtered = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > thresh:
            filtered.append(contour)
    return len(filtered) > 0, filtered
