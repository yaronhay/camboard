import cv2

GREEN = 0, 0xFF, 0
RED = 0, 0, 0xFF


def draw_paths(frame, paths):
    for path in paths:
        if len(path) < 2:
            continue
        i = 0
        while i < len(path) - 1:
            cv2.line(frame, path[i], path[i + 1], GREEN, 2)
            i += 1


def indicate_points(frame, paths, radius=1):
    for path in paths:
        if len(path) < 2:
            continue
        for point in path:
            cv2.circle(frame, point, radius, RED, 2)


class Display:
    def __init__(self, size, path='img/board75%.png'):
        self.__board = cv2.imread(path)
        cv2.rotate(self.__board, cv2.ROTATE_90_CLOCKWISE, self.__board)

        self.__f_height, self.__f_width = size
        self.__b_height, self.__b_width, _ = self.__board.shape

    def place_point(self, x, y):
        new_x = self.__b_height * (x / self.__f_height)
        new_y = self.__b_width * (y / self.__f_width)
        return int(new_x), int(new_y)

    def draw(self, paths):
        frame = self.__board.copy()

        draw_paths(frame, paths)
        indicate_points(frame, paths)

        return frame


def draw_point(frame, x, y, dx, dy, radius=5, color=GREEN):
    cv2.circle(frame, (x + dx, y + dy), radius, color, -1)
    return frame


def draw_polygon(frame, path, color=RED):
    i = 0
    while i < len(path) - 1:
        cv2.line(frame, path[i], path[i + 1], color, 2)
        i += 1
    cv2.line(frame, path[-1], path[0], color, 2)