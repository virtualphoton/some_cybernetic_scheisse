import websockets
import asyncio
from websockets.exceptions import ConnectionClosedError


def no_connection_handler(func):
    async def inner(*args, **kwargs):
        while True:
            try:
                return await func(*args, **kwargs)
            except (ConnectionClosedError, ConnectionRefusedError):
                print('no connection!')
                await asyncio.sleep(1)

    return inner


class Camera:
    def __init__(self):
        self.uri = "ws://localhost:8765"

    @no_connection_handler
    async def get_frame_from_socket(self):
        async with websockets.connect(self.uri) as websocket:
            return await websocket.recv()

    def get_frame(self):
        return asyncio.run(self.get_frame_from_socket())


class CommandSender:
    def __init__(self, port=8766):
        self.uri = f"ws://localhost:{port}"

    @no_connection_handler
    async def _send_command(self, jsoned):
        async with websockets.connect(self.uri) as websocket:
            await websocket.send(jsoned)
            return await websocket.recv()

    def send_command(self, jsoned):
        return asyncio.run(self._send_command(jsoned))
