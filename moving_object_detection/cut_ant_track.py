import cv2
from utils import vlogger
from utils.dataclass import DataClass
from utils.path_cutout import CutOutCropper
import utils.mycv2_utils as mycv2

from matplotlib import pyplot as plt

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
