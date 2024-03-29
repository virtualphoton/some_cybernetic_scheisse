import os.path
import sys

import pybullet as pb
import pybullet_data as pb_data

import asyncio

from machines.simulation.camera import Camera
from machines.simulation.robot import Robot
from machines.simulation.server import image_sender_server, command_communicator

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

physicsClient = pb.connect(pb.DIRECT)


def reset_and_start_sim():
    pb.setAdditionalSearchPath(pb_data.getDataPath())
    # plane = pb.loadURDF("plane.urdf")
    robot = Robot()
    pb.setTimeStep(0.01)  # no idea what this does
    pb.setRealTimeSimulation(0)  # to iterate normally
    return robot


async def main():
    robot = reset_and_start_sim()
    camera = Camera()
    await asyncio.gather(robot.move(),
                         image_sender_server(camera),
                         command_communicator(robot, camera))

    # to prevent some bugs with asyncio not closing loop
    await asyncio.sleep(0.1)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
    asyncio.get_event_loop().run_forever()
