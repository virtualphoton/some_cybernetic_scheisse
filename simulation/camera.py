import pybullet as pb


class Camera:
    default_size = {
        'width': 400,
        'height': 400
    }

    def __init__(self, size=None):
        if size is None:
            size = Camera.default_size

        self.viewMatrix = pb.computeViewMatrix(
            cameraEyePosition=[0, 0, 5],
            cameraTargetPosition=[0, 0, 0],
            cameraUpVector=[0, 1, 0])
        self.projectionMatrix = pb.computeProjectionMatrixFOV(
            fov=60.0,
            aspect=1.0,
            nearVal=0.1,
            farVal=100)
        self.cam_image_kwargs = {
            **size,
            'viewMatrix': self.viewMatrix,
            'projectionMatrix': self.projectionMatrix,
            'renderer': pb.ER_TINY_RENDERER
        }

    def get_frame(self):
        return pb.getCameraImage(**self.cam_image_kwargs)[2]
