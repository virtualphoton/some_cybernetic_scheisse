import websockets
import asyncio


class Camera:
    def __init__(self):
        self.uri = "ws://localhost:8765"

    async def get_frame_from_socket(self):
        async with websockets.connect(self.uri) as websocket:
            return await websocket.recv()

    def get_frame(self):
        return asyncio.run(self.get_frame_from_socket())


class CommandSender:
    def __init__(self):
        self.uri = "ws://localhost:8766"

    async def _send_command(self, jsoned):
        async with websockets.connect(self.uri) as websocket:
            await websocket.send(jsoned)
            return await websocket.recv()

    def send_command(self, jsoned):
        return asyncio.run(self._send_command(jsoned))
