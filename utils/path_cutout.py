import numpy as np
import cv2


def normalize_points(ul, pnts):
    ul_x, ul_y = ul
    res = []
    for x, y in pnts:
        res.append((x - ul_x, y - ul_y))
    return res


def create_cropping_settings(shape, pnts):
    # Frame height, Frame width, # of channels
    h, w, chan = shape

    # Minimal rectangle that bounds the points
    #   Input: A list of points each is a numpy array
    b_x, b_y, b_w, b_h = cv2.boundingRect(np.asarray(pnts))

    # Normalize all coordinates according to the new frame size (bounding rectangle)
    norm_points = normalize_points((b_x, b_y), pnts)

    # #
    # Create Mask
    # #
    mask = np.zeros((b_h, b_w, chan), dtype=np.uint8)

    # Fill the ROI (Region of Interest) so it doesn't get wiped out when the mask is applied
    roi_corners = np.array([norm_points], dtype=np.int32)
    ones = (0xFF,) * chan  # 1,...,1 (#chan times) for the and of the mask
    cv2.fillPoly(mask, roi_corners, ones)

    # #
    # Define cutout borders
    # #
    y0, y1 = b_y, b_y + b_h
    x0, x1 = b_x, b_x + b_w

    return {
        'mask': mask,
        'boarders': {
            'x': (x0, x1),
            'y': (y0, y1)
        }
    }


def cutout(frame, mask, x_b, y_b):
    (x0, x1), (y0, y1) = x_b, y_b
    return cv2.bitwise_and(frame[y0: y1, x0:x1], mask)


def cutout_by_defs(frame, defs):
    x_b, y_b = defs['boarders']['x'], defs['boarders']['y']
    return cutout(frame, defs['mask'], x_b, y_b)


class CutOutCropper:
    def __init__(self, shape, pnts):
        defs = create_cropping_settings(shape, pnts)
        self.mask = defs['mask']
        self.x_b, self.y_b = defs['boarders']['x'], defs['boarders']['y']
        self.__width = self.x_b[1] - self.x_b[0]
        self.__height = self.y_b[1] - self.y_b[0]

    @property
    def dimensions(self):
        return self.__width, self.__height

    def cutout(self, frame):
        return cutout(frame, self.mask, self.x_b, self.y_b)
