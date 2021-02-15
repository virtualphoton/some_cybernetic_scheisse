import websockets
import asyncio
import time
from websockets.exceptions import ConnectionClosedError
import json

FRAME_DELTA = 1 / 24


async def image_sender_server(camera):
    last_call_time = 0

    async def hello(websocket, path):
        nonlocal last_call_time
        if (delta := last_call_time + FRAME_DELTA - time.time()) > 0:
            await asyncio.sleep(delta)
        last_call_time = time.time()
        try:
            await websocket.send(camera.get_frame_bytes())
        except ConnectionClosedError:
            # has a chance to prevent this from falling
            pass

    await websockets.serve(hello, "localhost", 8765)


async def command_communicator(robot, camera):
    async def hello(websocket, path):
        try:
            jsoned = await websocket.recv()
            data = json.loads(jsoned.decode())
            command = data['command']
            args = data['args']
            if command == 'move_to':
                robot.set_new_coords(args)
                await websocket.send(json.dumps({'msg': 'Moving out!'}).encode())
            elif command == 'change_height':
                camera.set_new_height(args)
                await websocket.send(json.dumps({'msg': 'Success!'}).encode())

        except ConnectionClosedError:
            # has a chance to prevent this from falling
            pass

    await websockets.serve(hello, "localhost", 8766)
