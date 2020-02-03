from core import detector as detector

THRESHOLD = 70
COLOR_LIMITS = detector.BLUE_LIM


def core(front_c, top_c, menu_c, ph, displayer):
    QUARD = None
    ##
    # Determine if object is touching
    ##
    touching, contours = detector.detect_object_presence(top_c, COLOR_LIMITS, THRESHOLD)

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
        on_board, quard = detector.detect_object_location(front_c, COLOR_LIMITS)

        if on_board:
            ph.add_to_path(displayer.place_point(*quard))
            QUARD = quard

        else:
            on_menu, quard = False, None  # detector.detect_object_location(menu_c, COLOR_LIMITS)
            if on_menu:
                pass

    else:
        if ph.path_len > 1:
            ph.finish_path()
        else:
            ph.clear_path()

    return contours, QUARD
