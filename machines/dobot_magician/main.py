import sys

dll_path = r'C:\Users\bkmz1\Documents\books\robotics\dobot_lib'
sys.path.insert(1, dll_path)

import os.path
import sys
from server_communication import command_communicator
from robot import Robot, RobotCommunicator
import asyncio

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
robot = None


def main():
    global robot
    robot = Robot(dll_path)
    robot.connect()
    robot_com = RobotCommunicator(robot)
    commands = {
        'move_xyz': robot_com.move_xyz,
        'connect': lambda *args, **kwargs: None,
        'disconnect': lambda *args, **kwargs: None
    }
    robot_com.move_xyz([0, -50, 50])
    asyncio.get_event_loop().run_until_complete(command_communicator(commands))
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
        pass
    finally:
        robot.disconnect()
