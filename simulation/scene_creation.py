import pybullet as pb
import pybullet_data as pb_data
import time

from simulation.camera import Camera
from simulation.robot import Robot

physicsClient = pb.connect(pb.GUI)


def reset_and_start_sim():
    pb.resetSimulation()
    pb.setAdditionalSearchPath(pb_data.getDataPath())
    plane = pb.loadURDF("plane.urdf")
    robot = Robot()
    pb.setGravity(0, 0, 0)  # everything should fall down
    pb.setTimeStep(0.01)  # this slows everything down, but let's be accurate...
    pb.setRealTimeSimulation(0)  # we want to be faster than real time :)
    return robot


def main():
    robot = reset_and_start_sim()
    camera = Camera()
    camera.get_frame()
    robot.move_to([5, 5])
    time.sleep(100)


if __name__ == '__main__':
    main()
