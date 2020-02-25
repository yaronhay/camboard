import cv2
import numpy as np

camera_index = 2
camera = cv2.VideoCapture(camera_index)

while True:  # Capture frame by frame
    ret, frame = camera.read()
    frame = cv2.flip(frame, 1)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([35, 140, 60]), np.array([255, 255, 180]))
    cimg = cv2.medianBlur(mask, 5)

    circles = cv2.HoughCircles(cimg, cv2.HOUGH_GRADIENT, 1, 20,
                               param1=50, param2=30, minRadius=0, maxRadius=0)

    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        # draw the outer circle
        cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
        # draw the center of the circle
        cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)

    # Display the resulting frame
    cv2.imshow('frame', cimg)
    if cv2.waitKey(33) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
