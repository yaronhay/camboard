import cv2


class StringError(Exception):
    pass


class VideoCaptureTupleIterable:
    def __init__(self, cap, n=2):
        self.cap = cap
        self.n = n
        self.prevs = [None for _ in range(n)]

    def __iter__(base):
        class Iterator:
            def __init__(self):
                self.prevs = [None for _ in range(base.n)]
                self.cap = base.cap
                for _ in range(base.n):
                    ret, frame = self.cap.read()
                    if ret:
                        self.put_frame(frame)
                    else:
                        raise StringError("Capture did not return a frame")

            def put_frame(self, frame):
                self.prevs.pop(0)
                self.prevs.append(frame)

            def __next__(self) -> tuple:
                if not self.cap.isOpened():
                    raise StopIteration()

                ret, frame = self.cap.read()
                if not ret:
                    raise StringError("Capture did not return a frame")

                ret = tuple(self.prevs)
                self.put_frame(frame=frame)
                return ret

        return Iterator()


class MultiVideoCaptureTupleIterable:
    def __init__(self, caps: dict, n=2):
        self.caps = caps
        self.n = n
        self.prevs = [None for _ in range(n)]

    def __iter__(base):
        class Iterator:
            def __init__(self):
                self.prevs = [None for _ in range(base.n)]
                self.caps = base.caps
                for _ in range(base.n):
                    ret, frames = self.read_frames()
                    if ret:
                        self.put_frames(frames)
                    else:
                        raise StringError("At least one capture did not return a frame")

            def put_frames(self, frames):
                self.prevs.pop(0)
                self.prevs.append(frames)

            def read_frames(self):
                total_ret, frames = True, dict()

                for key in self.caps:
                    ret, frame = self.caps[key].read()
                    frames[key] = frame
                    total_ret = (total_ret and ret)

                return total_ret, frames

            def are_caps_open(self):
                return all(cap.isOpened() for cap in self.caps.values())

            def __next__(self) -> tuple:
                if not self.are_caps_open():
                    raise StopIteration()

                ret, frames = self.read_frames()
                if not ret:
                    raise StringError("At least one capture did not return a frame")

                ret = tuple(self.prevs)
                self.put_frames(frames=frames)
                return ret

        return Iterator()


VERT_FLIP = 1
HORIZ_FLIP = 0
BOTH_FLIP = -1


def show_video_capture(cap, flip=VERT_FLIP):
    cap = cv2.VideoCapture(cap)

    while cap.isOpened():
        ret, frame = cap.read()

        frame = cv2.flip(frame, flip)

        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
