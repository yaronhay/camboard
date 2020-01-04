import cv2

from utils import mycv2_utils as mycv2, vlogger

# Create Capture
cap = cv2.VideoCapture(1)

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create Logger
logger = vlogger.VideoLogger(width=frame_width, height=frame_height,
                             caps={'camera'},
                             fourcc='MP4V', extension='mp4')

for prev, curr in mycv2.VideoCaptureTupleIterable(cap):
    # Display Frame
    out_frame = curr
    logger.log('camera', out_frame)
    cv2.imshow('Current', curr)
    cv2.imshow('Previous', curr)

    if cv2.waitKey(40) == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
logger.release()
