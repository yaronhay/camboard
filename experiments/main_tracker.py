import moving_object_detection.generic_tracker as gt
from moving_object_detection.algos.image_diff_multi_cam \
    import  do as do, \
    iterator as iterator, \
    iteration as iteration, \
    folder as folder_name
import cv2


def main():
    loc = f'vlog/{folder_name}'
    caps = {
        'top_camera': cv2.VideoCapture(1),
        'front_camera': cv2.VideoCapture(2)
    }
    tracker = gt.GenericTracker(caps=caps,
                                iterator=iterator, loc=loc, do=do)
    tracker.method = iteration
    tracker.do()

    for cap in caps.values():
        cap.release()
