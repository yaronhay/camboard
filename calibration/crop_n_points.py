import cv2
import numpy as np


def normalize_points(ul, pnts):
    ul_x, ul_y = ul
    res = []
    for x, y in pnts:
        res.append((x - ul_x, y - ul_y))
    return res


class PointCropper:
    def __init__(self, n=4, camera_index=1):
        self.n = n

        self.__camera = cv2.VideoCapture(camera_index)
        self.pnts = []
        self.curr_pnt = None
        self.l_i = 0

    color = (0, 255, 0)

    def draw(self, frame):
        cur_pnts = self.pnts + [self.curr_pnt] if self.curr_pnt is not None else self.pnts
        l = len(cur_pnts)

        if l < 2:
            return

        i = 1
        while i < l:
            cv2.line(frame, cur_pnts[i - 1], cur_pnts[i], PointCropper.color, 2)
            i += 1

    def track_mouse(self, event, x, y, flags, param):
        if self.l_i == 0:
            if event == cv2.EVENT_LBUTTONUP:
                self.curr_pnt = None
                self.pnts.append((x, y))
                self.l_i = 1
        elif 1 <= self.l_i <= (self.n - 2):
            if event == cv2.EVENT_LBUTTONUP:
                self.curr_pnt = None
                self.pnts.append((x, y))
                self.l_i += 1
            elif event == cv2.EVENT_MOUSEMOVE:
                self.curr_pnt = (x, y)
        elif self.l_i == (self.n - 1):
            if event == cv2.EVENT_LBUTTONUP:
                self.l_i = self.n
                self.pnts.append((x, y))
                self.pnts.append(self.pnts[0])
            elif event == cv2.EVENT_MOUSEMOVE:
                self.curr_pnt = (x, y)

    def get_points(self):
        return self.pnts[:-1].copy()

    @property
    def camera(self):
        return self.__camera

    def main(self):

        cv2.namedWindow('Camera')
        cv2.setMouseCallback('Camera', self.track_mouse)

        cropping = False
        mask = None
        b_x, b_y, b_w, b_h = None, None, None, None
        while True:  # Capture frame by frame
            ret, frame = self.__camera.read()

            # Our operations on the frame come here
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            frame = cv2.flip(frame, 1)
            f_copy = frame.copy()
            self.draw(f_copy)

            # Display the resulting frame
            cv2.imshow('Camera', f_copy)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('c'):
                self.pnts = []
                self.curr_pnt = None
                self.l_i = 0
                cropping = False
            elif key == ord('s'):
                b_x, b_y, b_w, b_h = cv2.boundingRect(np.asarray(self.pnts))
                norm_points = normalize_points((b_x, b_y), self.pnts[:-1])
                f_h, f_w, f_chan = frame.shape
                mask = np.zeros((b_h, b_w, f_chan), dtype=np.uint8)

                roi_corners = np.array([norm_points], dtype=np.int32)
                # fill the ROI so it doesn't get wiped out when the mask is applied

                ignore_mask_color = (255,) * f_chan
                cv2.fillPoly(mask, roi_corners, ignore_mask_color)
                # from Masterfool: use cv2.fillConvexPoly if you know it's convex

                cropping = True

            if cropping:
                cropped = cv2.bitwise_and(frame[b_y: b_y + b_h, b_x:b_x + b_w], mask)
                cv2.imshow('Cropped', cropped)

    def close(self):
        self.__camera.release()
        cv2.destroyAllWindows()
