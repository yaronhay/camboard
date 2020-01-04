import cv2
import utils.dataclass as datacls

camera_index = 2

pnts = []
curr_pnt = None
l_i = 0
color = (0, 255, 0)


def draw(frame):
    cur_pnts = pnts + [curr_pnt] if curr_pnt is not None else pnts
    l = len(cur_pnts)

    if l < 2:
        return

    i = 1
    while i < l:
        cv2.line(frame, cur_pnts[i - 1], cur_pnts[i], color, 2)
        i += 1


mouse_moving = False


def track_mouse(event, x, y, flags, param):
    global pnts, curr_pnt, mouse_moving, l_i
    if l_i < 4:
        if event == cv2.EVENT_LBUTTONDOWN:
            curr_pnt = (x, y)
            mouse_moving = True
        elif event == cv2.EVENT_MOUSEMOVE:
            if mouse_moving:
                curr_pnt = (x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            curr_pnt = None
            pnts.append((x, y))
            mouse_moving = False
            l_i += 1


def main():
    camera = cv2.VideoCapture(camera_index)
    cv2.namedWindow('frame')
    cv2.setMouseCallback('frame', track_mouse)

    while True:  # Capture frame by frame
        ret, frame = camera.read()

        # Our operations on the frame come here
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        frame = cv2.flip(frame, 1)
        draw(frame)

        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()
