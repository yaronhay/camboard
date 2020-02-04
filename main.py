import os
import sys
import json

import cv2

from utils.path_cutout import CutOutCropper


def conf_file(conf_id):
    return f"conf/{conf_id}.conf.json"


def main():
    act = sys.argv[1]

    if act == "view":
        cam = int(sys.argv[2])

        import utils.mycv2_utils as mycv2
        mycv2.show_video_capture(cap=cam)

    elif act == "ncrop":
        import calibration.crop_n_points as cnp

        cam = int(sys.argv[2])
        n = 4
        cropper = cnp.PointCropper(n=n, camera_index=cam)
        cropper.main()
        cropper.close()

    elif act == "rectcrop":
        import calibration.crop_rectangle as cr

        cam = int(sys.argv[2])
        cropper = cr.RectangleCropper(camera_index=cam)
        cropper.main()
        cropper.close()

    elif act == "oldtrack":
        import moving_object_detection.cut_ant_track as ct

        conf_file_name = conf_file(conf_id=sys.argv[2])
        with open(conf_file_name) as file:
            conf = json.load(file)

        front = int(sys.argv[3])
        top = int(sys.argv[4])

        caps = {
            'top_camera': cv2.VideoCapture(top),
            'front_camera': cv2.VideoCapture(front)
        }

        ct.cut_and_track_color(conf, caps, isLogging=True)

        for cap in caps.values():
            cap.release()

    elif act == "track":
        import core.main as ct

        conf_file_name = conf_file(conf_id=sys.argv[2])
        with open(conf_file_name) as file:
            conf = json.load(file)

        front = int(sys.argv[3])
        top = int(sys.argv[4])

        caps = {
            'top_camera': cv2.VideoCapture(top),
            'front_camera': cv2.VideoCapture(front)
        }

        ct.do(conf, caps)

        for cap in caps.values():
            cap.release()

    elif act == "conf":
        conf_id = sys.argv[2]
        cnf_act = sys.argv[3]

        file_name = conf_file(conf_id=conf_id)

        if os.path.exists(file_name) and os.path.isfile(file_name):
            with open(file_name) as file:
                conf = json.load(file)
        else:
            conf = dict()

        if cnf_act == 'bcalib':
            import calibration.calibrate as calib

            cams = [
                {
                    'idx': int(sys.argv[4]),
                    'name': 'front_camera'
                },
                {
                    'idx': int(sys.argv[4]),
                    'name': 'menu_camera'
                },
                {
                    'idx': int(sys.argv[5]),
                    'name': 'top_camera'
                }
            ]
            conf['calibration'] = calib.board_calibrate(cams)

        elif cnf_act == 'mcalib':
            import calibration.calibrate as calib
            cnf = conf['calibration']['menu_camera']
            shape = cnf['height'], cnf['width'], cnf['channels']
            cropper = CutOutCropper(shape, cnf['points'])

            camera = cv2.VideoCapture(int(sys.argv[4]))
            r, frame = camera.read()
            assert r
            camera.release()

            frame = cropper.cutout(frame)

            conf['menu'] = calib.menu_calibrate(frame)
        else:
            print('No such operation')
            exit(1)

        with open(file_name, 'w') as file:
            json.dump(conf, file, indent=4)

    else:
        print('No such operation')
        exit(1)


if __name__ == '__main__':
    main()
