from core import detector as detector
import shapely.geometry

from utils.classes import PointHolder

THRESHOLD = 70
COLOR_LIMITS = detector.BLUE_LIM


def find_button(x, y, menu_buttons):
    for limits in menu_buttons:
        if x in range(*limits):
            return menu_buttons[limits]


def core(front_c, top_c, menu_c, displayer, state):
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
                point = shapely.geometry.Point(*board_location)
                for path in ph.paths[:-1]:
                    ls = shapely.geometry.LineString(path['points'])
                    if point.intersects(ls):
                        to_erase.append(path)
                ph.remove_paths(to_erase)
            else:
                ph.add_to_path(board_location)

        else:
            on_menu, menu_location = detector.detect_object_location(menu_c, COLOR_LIMITS)
            if on_menu:
                button = find_button(*menu_location, state.menu['buttons'])
                state.setcolor(button)

    else:
        if ph.path_len > 2:
            ph.finish_path()
        elif ph.path_len > 0:
            ph.clear_path()

    return top_contours, (menu_location, board_location)
