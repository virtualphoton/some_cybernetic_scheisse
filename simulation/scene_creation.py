import pybullet as pb
import pybullet_data as pb_data
import time

from simulation.camera import Camera
from simulation.robot import Robot

physicsClient = pb.connect(pb.GUI)


def reset_sim():
    pb.resetSimulation()
    pb.setAdditionalSearchPath(pb_data.getDataPath())
    plane = pb.loadURDF("plane.urdf")
    robot = Robot()
    return robot


def start_sim():
    pb.setGravity(0, 0, -10)  # everything should fall down
    pb.setTimeStep(0.01)  # this slows everything down, but let's be accurate...
    pb.setRealTimeSimulation(1)  # we want to be faster than real time :)


def main():
    reset_sim()
    start_sim()
    camera = Camera()
    camera.get_frame()
    time.sleep(100)


if __name__ == '__main__':
    main()
