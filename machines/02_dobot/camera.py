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
        self.captured_images = []
        
        self.dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
        self.parameters =  cv2.aruco.DetectorParameters()
        self.detector = aruco.ArucoDetector(self.dictionary, self.parameters)
        self.tile_size = 2 * .2 / 8
        self.board = aruco.CharucoBoard((8, 8), self.tile_size, self.tile_size / 2, self.dictionary)
        
        self.mtx, self.dist = None, None

    def set_pos(self, pos, up_vector, direction):
        pos = np.array(pos)
        up = np.cross(np.cross(direction, up_vector), direction)
        
        self.viewMatrix = pb.computeViewMatrix(
            cameraEyePosition=pos,
            cameraTargetPosition=pos + direction,
            cameraUpVector=up_vector
        )

    def get_frame(self, save=True) -> np.ndarray:
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
        frame = pb.getCameraImage(**params)[2][:, :, :3].astype(np.uint8)
        if save:
            self.captured_images.append(frame)
        return frame
    
    def calibrate(self):
        matched_points = []
        for image in self.captured_images:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cur_corners, cur_ids, _ = self.detector.detectMarkers(image)
            matched_points.append(list(
                map(np.squeeze, self.board.matchImagePoints(cur_corners, cur_ids))
            ))
        obj_points, img_points = zip(*matched_points)

        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
            obj_points, img_points, image.shape,
            None, None
        )
        self.mtx = mtx
        self.dist = dist
    
    def process_charuko(self, frame):
        assert self.mtx is not None and self.dist is not None
        
        frame = frame.copy()
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        corners, ids, _ = self.detector.detectMarkers(gray)
        
        if ids is None:
            cv2.putText(frame, "No Ids", (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)
            return frame
        
        _, corners_checker, ids_checker = aruco.interpolateCornersCharuco(
            corners, ids,
            gray, self.board
        )
        
        _, rvec, tvec = aruco.estimatePoseCharucoBoard(
            corners_checker, ids_checker, 
            self.board, self.mtx, self.dist,
            None, None
        )
        
        cv2.drawFrameAxes(frame, self.mtx, self.dist, rvec, tvec, 0.1)
        aruco.drawDetectedMarkers(frame, corners)
        rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, self.tile_size / 2, self.mtx, self.dist)
        
        for rvec, tvec in zip(rvecs, tvecs):
            cv2.drawFrameAxes(frame, self.mtx, self.dist, rvec, tvec, 0.03)
            
        return frame        
