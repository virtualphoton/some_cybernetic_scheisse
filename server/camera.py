import websockets
import asyncio


def image_bin(path):
    with open(path, 'rb') as f:
        return f.read()


# singleton
class Camera:
    @staticmethod
    async def get_frame_from_socket():
        uri = "ws://localhost:8765"
        async with websockets.connect(uri) as websocket:
            return await websocket.recv()

    @staticmethod
    def get_frame():
        return asyncio.run(Camera.get_frame_from_socket())
