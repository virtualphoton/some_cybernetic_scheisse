import os.path
import sys
import simulation
from server_communication import command_communicator
import asyncio
from serial_communication import Serial

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
-0.4, -1, 1.49
1.57,-1.57,0

def main():
    robot = simulation.start()
    ser = Serial()
    commands = {
        'connect': ser.send_start,
        'disconnect': ser.send_end,
        'move_to': lambda *args, **kwargs: ser.send_positions(robot.get_inverse_bytes(*args, **kwargs)),
    }
    input()
    ser.encase_and_send(b'\x00')
    asyncio.get_event_loop().run_until_complete(command_communicator(commands))
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()
