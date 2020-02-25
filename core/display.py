import cv2
import numpy as np

GREEN = 0, 0xFF, 0
RED = 0, 0, 0xFF
BLUE = 0xFF, 0, 0


def draw_path(frame, path, color):
    if len(path) < 2:
        return
    i = 0
    while i < len(path) - 1:
        cv2.line(frame, path[i], path[i + 1], color, 2)
        i += 1


def indicate_points(frame, path, radius=1):
    if len(path) < 2:
        return
    for point in path:
        cv2.circle(frame, point, radius, BLUE, 7)


class Display:
    def __init__(self, size, state):
        print(size)
        self.__state = state
        # self.__board = cv2.imread(path)
        self.__board = np.full((1080, 1920, 3), 0xFF, np.uint8)
        cv2.rectangle(self.__board, (0, 0), (1920, 1080), (128, 128, 128), thickness=70)
        cv2.rotate(self.__board, cv2.ROTATE_90_CLOCKWISE, self.__board)

        self.__f_width, self.__f_height = size
        print(self.__board.shape)
        self.__b_height, self.__b_width, _ = self.__board.shape


    def place_point(self, x, y):
        new_x = self.__b_width * (x / self.__f_width)
        new_y = self.__b_height * (y / self.__f_height)
        #print((x, y), (new_x, new_y))
        # assert new_x <= self.__b_width
        # assert new_y <= self.__b_height
        return int(new_x), int(new_y)

    def draw(self, paths):
        frame = self.__board.copy()

        for path in paths:
            points = path['points']
            color = path['color']

            points = list(map(lambda p: self.place_point(*p), points))

            draw_path(frame, points, color)
            indicate_points(frame, points)

        if self.__state.color is not None:
            color = self.__state.color
            cv2.rectangle(frame, (7, 7), (30, 30), color, cv2.FILLED)
            cv2.putText(frame, 'Color', (33, 33), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0))
        else:
            cv2.putText(frame, 'Eraser', (33, 33), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0))
        return frame


def draw_point(frame, x, y, dx=0, dy=0, radius=5, color=GREEN):
    cv2.circle(frame, (x + dx, y + dy), radius, color, -1)
    return frame


def draw_polygon(frame, path, color=RED):
    i = 0
    while i < len(path) - 1:
        cv2.line(frame, path[i], path[i + 1], color, 2)
        i += 1
    cv2.line(frame, path[-1], path[0], color, 2)
