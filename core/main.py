import time
import cv2
import core.display as display
from core.core_algorithm import core

from core.display import Display
from utils.classes import PointHolder
from utils.dataclass import DataClass
from utils.path_cutout import CutOutCropper


def iteration(displayer, cams, ph):
    front, top, menu = cams

    ##
    # Read Frames
    ##
    r, top_frame = top.camera.read()
    assert r

    r, front_frame = front.camera.read()
    assert r

    ##
    # Crop frames
    ##
    front_c = front.cropper.cutout(front_frame)
    top_c = top.cropper.cutout(top_frame)
    # menu_c = menu['cropper'].cutout(front_frame)

    ##
    # Core Operations
    ##
    contours, quard = core(front_c, top_c, None, ph, displayer)

    ##
    # Display Frames
    ##
    cv2.imshow('Board Drawing', displayer.draw(ph.paths))

    cv2.drawContours(top_c, contours, -1, display.GREEN, cv2.FILLED)
    cv2.imshow('Top Camera', top_c)

    display.draw_polygon(front_frame, front.points)
    if quard is not None:
        front_frame = display.draw_point(front_frame, *quard, *front.cropper.startpoint)
    cv2.imshow('Board Live', front_frame)


def main_loop(period, displayer, cams):
    ph = PointHolder()
    while all(cam.camera.isOpened() for cam in cams if cam is not None):
        start_time = time.time()

        iteration(displayer, cams, ph)

        end_time = time.time()
        loop_duration = round((end_time - start_time) * 1000)
        loop_duration_ms = period - int(loop_duration)
        time_left = loop_duration_ms if loop_duration_ms > 0 else 1

        key = cv2.waitKey(time_left)
        if key == ord('q'):
            break
        elif key == ord('c'):
            ph.clear()


def camera_setup(camera, calib):
    shape = calib['height'], calib['width'], calib['channels']
    pnts = calib['points']

    cropper = CutOutCropper(shape, pnts)

    return DataClass({
        'cropper': cropper,
        'shape': shape,
        'camera': camera,
        'points': [tuple(lst) for lst in pnts]
    })


def do(conf, caps):
    ##
    # Extract cameras
    ##
    front = camera_setup(caps['front_camera'], conf['calibration']['front_camera'])
    top = camera_setup(caps['top_camera'], conf['calibration']['top_camera'])
    menu = None  # camera_setup(caps['top_camera'], conf['calibration']['menu_camera'])

    ##
    # Init display
    ##
    displayer = Display(front.cropper.dimensions)

    ##
    # Main Loop
    ##
    fps = 30
    period = 1000 // fps
    main_loop(period, displayer, (front, top, menu))
