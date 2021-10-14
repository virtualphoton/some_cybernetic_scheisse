import pybullet as p


def start():
    # returns created in simulation robot's object
    p.connect(p.DIRECT)
    robot = Robot()
    return robot


class Robot:
    # class for a 6R arm defined in robot.urdf
    END_EFFECTOR_LINK = 9
    PATH = 'robot.urdf'

    def __init__(self):
        self.robot = p.loadURDF(self.PATH, useFixedBase=True)
        self.rev_joints = self.get_rev_joints()

    def get_inverse(self, pos, rpy=(0, 0, 0)):
        # returns list of new revolute joints' positions, given pos(x,y,z) and rpy of base ref. frame
        quaternion = p.getQuaternionFromEuler(rpy)
        return p.calculateInverseKinematics(self.robot, self.END_EFFECTOR_LINK, pos, quaternion)

    def get_rev_joints(self):
        # returns list of revolute joints
        return [i for i in range(10) if p.getJointInfo(self.robot, i)[2] == p.JOINT_REVOLUTE]
