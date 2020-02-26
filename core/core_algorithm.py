import os
from datetime import datetime, timedelta

import numpy as np

from core import detector as detector

from utils.classes import PointHolder

THRESHOLD = 0
COLOR_LIMITS = detector.RED_LIM
EPS = 5
MIN_TIME_DELTA = timedelta(seconds=3)

screenshot_time_stamp = datetime.now()
board_pen_time_stamp = datetime.now()


def find_button(x, y, menu_buttons):
    for limits in menu_buttons:
        if x in range(*limits):
            return menu_buttons[limits]


def core(front_c, top_c, menu_c, displayer, state):
    global screenshot_time_stamp, board_pen_time_stamp
    ph: PointHolder = state.ph
    color = state.color
    is_eraser = color is None
    board_location, menu_location = None, None
    ##
    # Determine if object is touching
    ##
    touching, top_contours = detector.detect_object_presence(top_c, COLOR_LIMITS, THRESHOLD)

    ##
    # IF touching any:
    # | IF pen ON board:
    # | |   APPEND pen.quards TO path
    # | |
    # | ELSE IF pen ON menu:
    # | |   buttons : point -> button MATCH-FUNCTION
    # | |                   = ALGORITHM(boarder : border -> (colors U eraser) DICTIONARY)(
    # | |                               FOR border in borders:
    # | |                               |   IF point IN border:
    # | |                               |   |   YIELD match(borders)
    # | |                              )
    # | |   selected := buttons.match(pen.quards)
    # | |
    # | |   IF selected == eraser:
    # | |   |   SET eraser mode ON
    # | |   ELSE IF selected IN colors:
    # | |   |   SET paint_color TO color(selected)
    # | |
    # | |
    # ELSE:
    # | IF LEN(path) > 1:
    # | |   SUBMIT path
    # | ELSE:
    # | |   CLEAR path
    # | |
    ##
    if touching:
        on_board, board_location = detector.detect_object_location(front_c, COLOR_LIMITS)

        if on_board:
            if is_eraser:
                to_erase = []
                point = np.asarray(board_location)
                for path in ph.paths[:-1]:
                    points = [np.asarray(p) for p in path['points']]
                    if is_point_close_to_path(points, point, eps=EPS):
                        to_erase.append(path)
                ph.remove_paths(to_erase)

            else:
                ph.add_to_path(board_location)

        else:
            on_menu, menu_location = detector.detect_object_location(menu_c, COLOR_LIMITS)
            if on_menu:
                button = find_button(*menu_location, state.menu['buttons'])
                if button == 'camera':
                    now = datetime.now()
                    delta = now - screenshot_time_stamp
                    screenshot_time_stamp = now

                    if delta > MIN_TIME_DELTA:
                        print("in")
                        subject = 'Your Boardshot'
                        content = 'Here is you boardshot - the screenshot of your smart board, ' \
                                  f'taken on {now.strftime("%c")}:'
                        address = 'yaron.hay@live.biu.ac.il'
                        file_name = f"Boardshot{now.strftime('%Y_%m_%d_%H_%M_%S')}.png"

                        os.system(f"screencapture {file_name}")
                        print(content)
                        os.system(f"./core/email.sh {address} \"{subject}\" \"{content}\" {file_name}")
                else:
                    state.setcolor(button)


    else:
        if ph.path_len > 2:
            ph.finish_path()
        elif ph.path_len > 0:
            ph.clear_path()

    return top_contours, (menu_location, board_location)


# def is_point_on_line(p, p1, p2):
#     x,y= p
#     x1, y1 = p1,
#     x2, y2 = p2
#
#     if y1 > y2:
#         y1, y2 = y2, y1
#
#     if x1 == x2:
#         return x == x1 and y1 <= y <= y2
#     else:

# https://diego.assencio.com/?index=ec3d5dfdfc0b6a0d147a656f0af332bd
def closest_point(x, p, q):
    # line s = p + lamb*(q - p)
    qmp = q - p

    # lamb = ((x-p)*(q-p))/((q-p)*(q-p))
    numerator = np.dot(x - p, qmp)
    denominator = np.dot(qmp, qmp)

    if numerator <= 0:  # lamb <= 0:
        return p
    elif numerator >= denominator:  # lamb >= 1
        return q
    else:  # 0 < lamb < 1
        lamb = numerator / denominator
        return p + lamb * qmp


def is_point_close_to_path(path, point, eps):
    epssq = eps * eps
    i = 0
    lim = len(path) - 1
    while i < lim:
        closest = closest_point(point, path[i], path[i + 1])
        delta = point - closest
        inner = np.inner(delta, delta)
        # print(f'point{point} closest{closest} dist{inner} line: {path[i]}-{path[i + 1]}')
        if inner < epssq:
            # print(True)
            return True

        i += 1
    return False
