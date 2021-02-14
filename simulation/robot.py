import pybullet as pb


class Robot:
    def __init__(self):
        cube_start_pos = [0, 0, 1]
        cube_start_orientation = pb.getQuaternionFromEuler([0, 0, 0])
        self.robot_obj = pb.loadURDF("r2d2.urdf", cube_start_pos, cube_start_orientation)
