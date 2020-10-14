import cv2
from utils import vlogger

from utils.dataclass import DataClass


class GenericTracker:
    def __init__(self, caps: dict, iterator, loc=".", do=None):

        # Create Capture
        self.caps = caps

        fsizes = {
            key: DataClass({
                "width": int(self.caps[key].get(cv2.CAP_PROP_FRAME_WIDTH)),
                "height": int(self.caps[key].get(cv2.CAP_PROP_FRAME_HEIGHT))
            })
            for key in self.caps}

        # Create Logger
        self.logger = vlogger.VideoLogger(loc=loc)

        # Save Objects
        self.method = lambda item, data: None
        self.iterable = iterator(self.caps)

        self.data = DataClass({
            'frame_sizes': fsizes,
            'logger': self.logger
        })

        if do is not None:
            do(self.data)

    def do(self):
        for item in self.iterable:
            self.method(item, self.data)
            if cv2.waitKey(40) == ord('q'):
                break

        cv2.destroyAllWindows()
        self.logger.release()
