import pybullet as pb
import pybullet_data as pb_data

import asyncio

from simulation.camera import Camera
from simulation.robot import Robot
from simulation.server import start_server_loop

physicsClient = pb.connect(pb.DIRECT)


def reset_and_start_sim():
    pb.resetSimulation()
    pb.setAdditionalSearchPath(pb_data.getDataPath())
    plane = pb.loadURDF("plane.urdf")
    robot = Robot()
    pb.setTimeStep(0.01)  # no idea what this does
    pb.setRealTimeSimulation(0)  # to iterate normally
    return robot


async def main():
    robot = reset_and_start_sim()
    camera = Camera()
    await asyncio.gather(robot.move_to([3, 3]),
                         start_server_loop(camera))

    # to prevent some bugs with asyncio not closing loop
    await asyncio.sleep(0.1)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
    asyncio.get_event_loop().run_forever()
