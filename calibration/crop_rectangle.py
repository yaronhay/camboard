import cv2


class RectangleCropper:
    def __init__(self, camera_index=1):
        self.mouse_moving = False
        self.start = None
        self.end = None
        self.camera = cv2.VideoCapture(camera_index)

    color = (0, 255, 0)

    def draw(self, frame):
        if self.start is not None:
            cv2.rectangle(frame, self.start, self.end, RectangleCropper.color, 2)

    def track_mouse(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN:
            self.start = (x, y)
            self.mouse_moving = True
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.mouse_moving:
                self.end = (x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            self.end = (x, y)
            self.mouse_moving = False

    def main(self):
        cv2.namedWindow('Original')
        cv2.setMouseCallback('Original', self.track_mouse)

        cropping = False
        ul = [None, None]
        br = [None, None]

        while True:  # Capture frame by frame
            ret, frame = self.camera.read()

            # Our operations on the frame come here
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            frame = cv2.flip(frame, 1)
            drawn = frame.copy()
            self.draw(drawn)

            # Display the resulting frame
            cv2.imshow('Original', drawn)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('c'):
                self.start = self.end = None
                cropping = False
            elif key == ord('s'):
                ul[0] = min(self.start[0], self.end[0])  # min x
                ul[1] = min(self.start[1], self.end[1])  # min y

                br[0] = max(self.start[0], self.end[0])  # max x
                br[1] = max(self.start[1], self.end[1])  # max y

                cropping = True

            if cropping:
                crop = frame[ul[1]:br[1], ul[0]:br[0]]  # [y:y+h, x:x+w]
                cv2.imshow('Cropped', crop)

    def close(self):
        self.camera.release()
        cv2.destroyAllWindows()
