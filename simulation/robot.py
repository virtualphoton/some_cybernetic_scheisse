import pybullet as pb
import numpy as np
import time
from simulation.useful_funcs import normalize

from simulation.camera import Camera


class Robot:
    ALPHA = 2000

    def __init__(self):
        cube_start_pos = [0, 0, 1]
        cube_start_orientation = pb.getQuaternionFromEuler([0, 0, 0])
        self.robot = pb.loadURDF("r2d2.urdf", cube_start_pos, cube_start_orientation)

    def move_to(self, new_coords):
        if len(new_coords) == 2:
            new_coords = list(new_coords) + [0]
        new_coords = np.array(new_coords)
        pb.resetBaseVelocity(self.robot, (0, 0, 0))
        while True:
            pb.stepSimulation()
            time.sleep(1 / 240)
            obj_coords = pb.getBasePositionAndOrientation(self.robot)[0]
            force = np.array(obj_coords) - np.array(new_coords)
            force[2] = 0
            if np.linalg.norm(force) < 0.1:
                pb.resetBaseVelocity(self.robot, (0, 0, 0))
                return
            force = normalize(force)
            self.check_bounds()
            pb.applyExternalForce(self.robot, linkIndex=-1, forceObj=-Robot.ALPHA * force, posObj=obj_coords,
                                  flags=pb.WORLD_FRAME)

    def check_bounds(self):
        k = 1
        coords = pb.getBasePositionAndOrientation(self.robot)[0]
        if not (-10 <= coords[0] <= 10 and -10 <= coords[1] <= 10):
            pb.resetBaseVelocity(self.robot, -k * np.array(pb.getBaseVelocity(self.robot)[0]))
