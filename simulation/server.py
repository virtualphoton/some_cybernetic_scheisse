import websockets
import asyncio
import time

FRAME_DELTA = 1 / 24


async def start_server_loop(camera):
    last_call_time = 0

    async def hello(websocket, path):
        nonlocal last_call_time
        if (delta := last_call_time + FRAME_DELTA - time.time()) > 0:
            await asyncio.sleep(delta)
        last_call_time = time.time()
        await websocket.send(camera.get_frame_bytes())

    await websockets.serve(hello, "localhost", 8765)
