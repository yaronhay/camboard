import cv2
import calibration.crop_n_points as cnp


def calibrate(cams):
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
