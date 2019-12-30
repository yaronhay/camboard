from datetime import datetime
import cv2
import os
import utils.dataclass as datacls

FOLDER_NAME = "video_log"


def create_log_folder(name=FOLDER_NAME):
    if not os.path.exists(name):
        os.makedirs(name)


def create_defs(frame_width, frame_height, fourcc, extension, fps):
    dims = (frame_width, frame_height)  # According to cv2 first Width then Height
    codec = {
        'extension': extension,
        'fourcc': cv2.VideoWriter_fourcc(*fourcc)
    }
    return datacls.DataClass({
        'dims': dims,
        'codec': datacls.DataClass(codec),
        'fps': fps
    })


class VideoLogger:
    def __init__(self, loc=FOLDER_NAME, ):
        self.path = f"{loc}/{datetime.now()}"
        create_log_folder(self.path)

        self.writers = {}
        self.indices = {}

    def add(self, name, defs):
        file_name = f"{self.path}/{name}.{defs.codec.extension}"

        self.writers[name] = cv2.VideoWriter(file_name, defs.codec.fourcc, defs.fps, defs.dims)
        self.indices[name] = datacls.DataClass({
            'log': lambda frame: self.log(name, frame)
        })

    def log(self, cap, frame):
        self.writers[cap].write(frame)

    def release(self):
        for cap in self.writers.values():
            cap.release()

    def __getitem__(self, item):
        return self.indices[item]
