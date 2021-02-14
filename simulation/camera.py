import pybullet as pb
from PIL import Image as im
import asyncio


class Camera:
    TIME_DELTA = 1/10
    PATH = r'C:\Users\bkmz1\Documents\books\python\some_cybernetic_scheisse\out.jpg'

    default_size = {
        'width': 400,
        'height': 400
    }

    def __init__(self, size=None):
        if size is None:
            size = Camera.default_size

        self.viewMatrix = pb.computeViewMatrix(
            cameraEyePosition=[0, 0, 10],
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

    def write_frame(self, frame):
        im.fromarray(frame).convert('RGB').save(Camera.PATH, "JPEG", quality=80, optimize=True, progressive=True)

    async def get_and_write_frame_loop(self):
        """
        takes photo from camera and writes it to 'out.jpg' file
        then sleeps to make 24 fps
        """
        while True:
            self.write_frame(self.get_frame())
            await asyncio.sleep(Camera.TIME_DELTA)
