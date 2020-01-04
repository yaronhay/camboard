import cv2
import utils.dataclass as datacls

camera_index = 2
camera = cv2.VideoCapture(camera_index)

lines = []
curr_line = None
color = (0, 255, 0)



def draw(frame):
    global lines, curr_line

    for line in (lines + [curr_line] if curr_line is not None else lines):
        cv2.line(frame, line.start, line.end, color, 3)


mouse_moving = False


def track_mouse(event, x, y, flags, param):
    global lines, curr_line, mouse_moving

    if event == cv2.EVENT_LBUTTONDOWN:
        curr_line = datacls.DataClass({
            'start': (x, y),
            'end': (x, y)
        })
        mouse_moving = True
    elif event == cv2.EVENT_MOUSEMOVE:
        if mouse_moving:
            curr_line.end = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        curr_line.end = (x, y)
        lines.append(curr_line)
        curr_line = None
        mouse_moving = False


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
