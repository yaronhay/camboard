import moving_object_detection.generic_tracker as gt
from utils import mycv2_utils as mycv2
import cv2
from utils import vlogger

__cam_names = {
    'top_camera',
    'front_camera'
}


def do(data):
    logger = data.logger

    topsize = data.frame_sizes['top_camera']
    defs = vlogger.create_defs(
        frame_width=topsize.width,
        frame_height=topsize.height,
        fourcc='XVID', extension='mp4', fps=30.)
    logger.add('top_camera', defs)
    logger.add('top_camera_squares', defs)

    frontsize = data.frame_sizes['front_camera']
    defs = vlogger.create_defs(
        frame_width=frontsize.width,
        frame_height=frontsize.height,
        fourcc='XVID', extension='mp4', fps=30.)
    logger.add('front_camera', defs)
    logger.add('front_camera_squares', defs)


def iteration(item, data):
    logger = data.logger

    frames1, frames2 = item
    for cam in __cam_names:
        frame1, frame2 = frames1[cam], frames2[cam]
        logger[cam].log(frame1)

        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            # 
            if cv2.contourArea(contour) < 900:
                continue
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 3)

        cv2.imshow(f"Rec {cam}", frame1)

        logger[f'{cam}_squares'].log(frame1)


folder = "image_diff_multi_cam"

iterator = lambda caps: mycv2.MultiVideoCaptureTupleIterable(caps, n=2)
