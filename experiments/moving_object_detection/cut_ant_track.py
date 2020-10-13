import cv2
import numpy as np

from utils import vlogger
from utils.dataclass import DataClass
from utils.path_cutout import CutOutCropper
import utils.mycv2_utils as mycv2

import time

# from matplotlib import pyplot as plt

folder_name = 'fname'

iterator = lambda caps: mycv2.MultiVideoCaptureTupleIterable(caps, n=2)


def do(data):
    conf = data.conf

    calibration = conf['calibration']
    data.croppers = dict()
    for cam, cnf in calibration.items():
        shape = cnf['height'], cnf['width'], cnf['channels']
        pnts = cnf['points']
        data.croppers[cam] = CutOutCropper(shape, pnts)

    if data.logger is not None:
        logger: vlogger.VideoLogger = data.logger
        for name, cap in data.caps.items():
            defs = vlogger.create_defs(
                frame_width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                frame_height=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                fourcc='XVID', extension='mp4', fps=30.)
            logger.add(name=name, defs=defs)

        for name, cropper in data.croppers.items():
            w, h = cropper.dimensions
            defs = vlogger.create_defs(
                frame_width=w, frame_height=h,
                fourcc='XVID', extension='mp4', fps=30.)
            logger.add(name=f'{name}_cropped', defs=defs)
            logger.add(name=f'{name}_diff', defs=defs)
            logger.add(name=f'{name}_contours', defs=defs)


green = (0, 255, 0)

fig = None


def method(item, data):
    global fig
    plt.close(fig)
    logged = dict()
    # Decouple frame param
    frames1, frames2 = item

    plots = list()

    for cam in ['top_camera', 'front_camera']:
        original_frame1, original_frame2 = frames1[cam], frames2[cam]

        cropper: CutOutCropper = data.croppers[cam]
        frame1, frame2 = cropper.cutout(original_frame1), cropper.cutout(original_frame2)

        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        contours_frame = frame1.copy()

        for contour in contours:
            if cv2.contourArea(contour) < 900:
                continue

            cv2.drawContours(contours_frame, [contour], -1, green, 3)

        # cv2.imshow(cam, frame1)
        # cv2.imshow(f'{cam}_diff', diff)
        # cv2.imshow(f'{cam}_contours', contours_frame)

        cv2.cvtColor(dilated, cv2.COLOR_GRAY2BGR)
        frame_dict = {
            cam: original_frame1,
            f'{cam}_cropped': frame1,
            f'{cam}_diff': diff,
            f'{cam}_contours': contours_frame
        }
        plots.append(frame_dict)
        logged.update(frame_dict)

        cv2.imshow(f'{cam}_cropped', frame1)
        cv2.imshow(f'{cam}_contours', contours_frame)

    # fig, ax = plt.subplots(nrows=len(plots), ncols=4)
    # for row, plot in zip(ax, plots):
    #     for cell, (name, img) in zip(row, plot.items()):
    #         cell.imshow(img)
    #         cell.set_title(name)
    # plt.show()

    # for name, img in plots.items():
    #    cv2.imshow(name, img)
    return logged


def cut_and_track(conf, caps, loc=".", isLogging=True):
    global folder_name, iterator  # , method
    loc = f'vlog/{folder_name}'

    data = DataClass({
        'caps': caps,
        'conf': conf
    })
    logger = data.logger = vlogger.VideoLogger(loc=loc) if isLogging else None

    do(data)
    iterable = iterator(caps)

    for item in iterable:

        logs = method(item, data)

        if isLogging:
            for name in logs:
                logger[name].log(logs[name])

        if cv2.waitKey(40) == ord('q'):
            break

    cv2.destroyAllWindows()
    logger.release()


def draw_paths(frame, paths):
    for path in paths:
        if len(path) < 2:
            continue
        i = 0
        while i < len(path) - 1:
            cv2.line(frame, path[i], path[i + 1], green, 2)
            i += 1


def draw_points(frame, paths):
    for path in paths:
        if len(path) < 2:
            continue
        for point in path:
            cv2.circle(frame, point, 1, (0, 0, 255), 2)


# HELP https://www.learnopencv.com/find-center-of-blob-centroid-using-opencv-cpp-python/
def cut_and_track_color(conf, caps, loc=".", isLogging=True):
    org = cv2.imread('img/board75%.png')
    cv2.rotate(org, cv2.ROTATE_90_CLOCKWISE, org)

    lower = np.array([35, 140, 60])
    upper = np.array([255, 255, 180])

    front_cap = caps['front_camera']
    front_cnf = conf['calibration']['front_camera']

    shape = front_cnf['height'], front_cnf['width'], front_cnf['channels']
    front_cropper = CutOutCropper(shape, front_cnf['points'])

    bh, bw, _ = org.shape
    ch, cw = front_cropper.dimensions
    cox, coy = front_cropper.startpoint

    def xy_to_board(x, y):
        new_x = bh * (x / ch)
        new_y = bw * (y / cw)
        xy = int(new_x), int(new_y)
        return xy

    def do_front(frame):
        cutout = front_cropper.cutout(frame)
        hsv = cv2.cvtColor(cutout, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        # result = cv2.bitwise_and(cutout, cutout, mask=mask)
        try:
            M = cv2.moments(mask)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            ret = cX, cY
            cv2.circle(frame, (cox + cX, coy + cY), 5, green, -1)
            # cv2.circle(board, xy_to_board(cX, cY), 5, green, -1)
            # cv2.putText(frame, "centroid", (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        except ZeroDivisionError:
            ret = None

        return ret

    top_cap = caps['top_camera']
    top_cnf = conf['calibration']['top_camera']

    top_shape = top_cnf['height'], top_cnf['width'], top_cnf['channels']
    top_cropper = CutOutCropper(top_shape, top_cnf['points'])

    def do_top(frame):
        cutout = top_cropper.cutout(frame)
        hsv = cv2.cvtColor(cutout, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        filtered = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if not area <= 70:
                filtered.append(contour)

        cv2.drawContours(cutout, filtered, -1, (0, 0, 255), cv2.FILLED)
        cv2.imshow('TOP_FILTERED', cutout)
        return len(filtered) > 0

    path = list()
    paths = list()
    while front_cap.isOpened() and top_cap.isOpened():
        start_time = time.time()
        board = org.copy()
        r= False
        while not r:
            r, top_frame = top_cap.read()
        # assert r
        r = False
        while not r:
            r, front_frame = front_cap.read()
        #assert r


        touching = do_top(top_frame)
        if touching:
            quard = do_front(front_frame)
            if quard is not None:
                quard = xy_to_board(*quard)
                path.append(quard)
        elif len(path) > 0:
            paths.append(path)
            path = list()

        draw_paths(board, paths + [path])
        draw_points(board, paths + [path])

        # cv2.imshow('mask', mask)
        # cv2.imshow('cutout', cutout)
        cv2.imshow('Board', front_frame)
        cv2.imshow('Image Board', board)

        end_time = time.time()
        loop_duration = round((end_time - start_time) * 1000)
        time_left = (1000 // 30) - int(loop_duration)
        if time_left <= 0:
            time_left = 1

        key = cv2.waitKey(time_left)
        if key == ord('q'):
            break
        elif key == ord('c'):
            paths.clear()
