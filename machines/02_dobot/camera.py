import pybullet as pb
from PIL import Image as im
import io
import cv2
import numpy as np
import cv2.aruco as aruco

class Camera:
    QUALITY = 80

    default_size = {
        'width': 1280,
        'height': 720
    }

    def __init__(self, size=None):
        if size is None:
            size = Camera.default_size
        self.size = size
        self.viewMatrix = None
        
        self.projectionMatrix = pb.computeProjectionMatrixFOV(
            fov=90.0,
            aspect=1280 / 720,
            nearVal=0.1,
            farVal=100
        )

    def set_pos(self, pos, up_vector, delta):
        pos = np.array(pos)
        self.viewMatrix = pb.computeViewMatrix(
            cameraEyePosition=pos,
            cameraTargetPosition=pos + delta,
            cameraUpVector=up_vector
        )

    def get_frame(self) -> np.ndarray:
        """
        returns RGBA array of size (x, y, 4)
        """
        if self.viewMatrix is None:
            return np.array([])
        params = {
            **self.size,
            'viewMatrix': self.viewMatrix,
            'projectionMatrix': self.projectionMatrix,
            'renderer': pb.ER_BULLET_HARDWARE_OPENGL
        }
        return pb.getCameraImage(**params)[2]
    
    
    def get_arucos(self, frame, prt=False):
        frame = frame[:, :, :3].astype(np.uint8)
        if prt:
            cv2.imwrite("arucos.png", frame)
            print(1)
        
        mtx = np.array([[6.18050259e+05, 0.00000000e+00, 6.39488488e+02],
        [0.00000000e+00, 6.18050677e+05, 3.59501727e+02],
        [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
        dist = np.array([[ 8.07480697e-01,  7.50618764e-07, -8.02591978e-05,
            5.02494853e-05,  5.98330140e-13]])
        
        font = cv2.FONT_HERSHEY_SIMPLEX

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
        board = aruco.CharucoBoard_create(8, 8, .4, .2, aruco_dict)
        parameters =  aruco.DetectorParameters_create()
        corners, ids, _ = aruco.detectMarkers(
            gray,
            aruco_dict,
            parameters=parameters
        )
        
        if ids is None:
            cv2.putText(frame, "No Ids", (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)
            return frame
        
        _, corners_checker, ids_checker = aruco.interpolateCornersCharuco(
            corners,
            ids,
            gray,
            board
        )
        res, rvec, tvec = aruco.estimatePoseCharucoBoard(
            corners_checker, ids_checker, board,
            mtx, dist,
            np.zeros(3), np.zeros(3)
        )
        
        if prt:
            rvec, tvec = rvec.reshape(1, -1), tvec.reshape(1, -1)
            print(rvec / np.linalg.norm(rvec, axis=1, keepdims=True) * np.sign(rvec[:, :1]))
            print()
            for rvec_ in rvec:
                print(cv2.Rodrigues(rvec_)[0])
                print()
            print("---------------------------------")
            
            print(tvec)
            return frame
        
        cv2.drawFrameAxes(frame, mtx, dist, rvec, tvec, 0.4)
        aruco.drawDetectedMarkers(frame, corners)
        
        rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, 0.2, mtx, dist)
        
        for i in range(rvec.shape[0]):
            cv2.drawFrameAxes(frame, mtx, dist, rvec[i], tvec[i], 0.03)
            
        return frame        
