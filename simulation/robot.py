import pybullet as pb
import numpy as np
from simulation.useful_funcs import normalize
import asyncio


class Robot:
    ALPHA = 1500
    MAX_SPEED = 5
    TIME_DELTA = 1 / 240

    def __init__(self):
        cube_start_pos = [0, 0, 1.5]
        cube_start_orientation = pb.getQuaternionFromEuler([0, 0, 0])
        self.robot = pb.loadURDF("r2d2.urdf", cube_start_pos, cube_start_orientation)

    async def move_to(self, new_coords):
        """
        moves objects to selected coordinated
        :param new_coords: (x, y)
        """
        new_coords = np.array(list(new_coords) + [0])
        pb.resetBaseVelocity(self.robot, (0, 0, 0))
        while True:
            pb.stepSimulation()

            obj_coords = self.get_pos()
            obj_new_coords = obj_coords.copy()
            obj_new_coords[2] = 0
            # stop motion
            if np.linalg.norm(obj_new_coords - new_coords) < 0.1:
                pb.resetBaseVelocity(self.robot, (0, 0, 0))
                return

            # move
            self.check_bounds()
            pb.applyExternalForce(self.robot, linkIndex=-1, forceObj=self.get_force(new_coords), posObj=obj_coords,
                                  flags=pb.WORLD_FRAME)

            await asyncio.sleep(Robot.TIME_DELTA)

    def check_bounds(self):
        """
        check if object is inside 10x10 area and bounces it back if not
        :return:
        """
        k = 1
        coords = pb.getBasePositionAndOrientation(self.robot)[0]
        if not (-10 <= coords[0] <= 10 and -10 <= coords[1] <= 10):
            pb.resetBaseVelocity(self.robot, -k * np.array(pb.getBaseVelocity(self.robot)[0]))

    def get_pos(self):
        """
        returns pos of object
        :return: numpy array
        """
        return np.array(pb.getBasePositionAndOrientation(self.robot)[0])

    def get_force(self, new_coords):
        """
        force to push to new coords
        :param new_coords: np.array of (x, y, z)
        :return: force
        """
        if np.linalg.norm(pb.getBaseVelocity(self.robot)[0]) > Robot.MAX_SPEED:
            return (0, 0, 0)
        force = self.get_pos() - new_coords
        force[2] = 0
        return -Robot.ALPHA * normalize(force)
