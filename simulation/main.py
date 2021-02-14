import pybullet as pb
import pybullet_data as pb_data

import asyncio

from simulation.camera import Camera
from simulation.robot import Robot

physicsClient = pb.connect(pb.DIRECT)


def reset_and_start_sim():
    pb.resetSimulation()
    pb.setAdditionalSearchPath(pb_data.getDataPath())
    plane = pb.loadURDF("plane.urdf")
    robot = Robot()
    pb.setGravity(0, 0, 0)  # everything should fall down
    pb.setTimeStep(0.01)  # this slows everything down, but let's be accurate...
    pb.setRealTimeSimulation(0)  # we want to be faster than real time :)
    return robot


async def main():
    robot = reset_and_start_sim()
    camera = Camera()
    await asyncio.gather(robot.move_to([3, 3]),
                         camera.get_and_write_frame_loop())

    # to prevent some bugs with asyncio not closing lopo
    await asyncio.sleep(0.1)


if __name__ == '__main__':
    asyncio.run(main())
