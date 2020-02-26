import calibration.crop_n_points as cnp
import cv2

from utils.mycv2_utils import paint_lines


def board_calibrate(cams):
    res = dict()
    for cam in cams:
        cam_cnf = dict()
        cropper = cnp.PointCropper(n=4, camera_index=cam['idx'])

        ret, frame = cropper.camera.read()
        cam_cnf['height'], cam_cnf['width'], cam_cnf['channels'] = frame.shape

        cropper.main()
        cropper.close()

        cam_cnf['points'] = cropper.get_points()

        res[cam['name']] = cam_cnf

    return res


colors = {
    'blue': (255,191,0),
    'black': (0, 0, 0),
    'orange': (0, 0x8C, 0xFF),
    'green': (0, 0xFF, 0),
    'eraser': None,
    'camera': 'camera'
}


def menu_calibrate(frame):
    height, width, _ = frame.shape

    line = None
    lines = [0, width]

    def track_mouse(event, x, y, flags, param):
        nonlocal line, lines
        if event == cv2.EVENT_LBUTTONDOWN:
            lines.append(x)
        elif event == cv2.EVENT_MOUSEMOVE:
            line = x

    cv2.namedWindow('Menu')
    cv2.setMouseCallback('Menu', track_mouse)

    while True:
        f_copy = frame.copy()
        paint_lines(f_copy, height, lines + [line])

        cv2.imshow('Menu', f_copy)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            lines = [0, width]

    lines.sort()

    result = list()
    for i in range(1, len(lines)):
        color = input(f'Color of button #{i}:')
        result.append({
            'bottom': lines[i - 1],
            'upper': lines[i],
            'color': colors[color.strip().lower()]
        })
    return result
