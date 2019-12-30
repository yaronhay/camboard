import cv2
import calibration.crop_n_points as cnp


def calibrate(cams):
    res = dict()
    for cam in cams:
        cam_cnf = dict()
        cropper = cnp.PointCropper(n=4, camera_index=cam['idx'])

        cam_cnf['width'] = int(cropper.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        cam_cnf['height'] = int(cropper.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

        cropper.main()
        cropper.close()

        cam_cnf['points'] = cropper.get_points()

        res[cam['name']] = cam_cnf

    return res
