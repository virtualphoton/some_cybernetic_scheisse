import json
import os
import asyncio

import websockets
from websockets.exceptions import ConnectionClosedError

import DobotDllType as dT
os.environ["LD_LIBRARY_PATH"] = ":/usr/DobotDllOutput"


api = dT.load()
connected = not dT.ConnectDobot(api, "192.168.43.221", 115200)[0]
if not connected:
    raise RuntimeError("couldt't connect")
print("potentialy connected, sending init commands... (if hasn't printed 'ready' in several seconds, then restart)")

dT.SetQueuedCmdClear(api)
dT.SetHOMEParams(api, 200, 200, 200, 200, isQueued = 1)
print("ready!")
print(dT.GetPose(api)[:3])

commands = {"get_xyz": lambda: dT.GetPose(api)[:3]}

async def command_communicator(commands):
    async def listener(websocket, path):
        try:
            jsoned = await websocket.recv()
            data = json.loads(jsoned)
            print(data)
            res = commands[data['command']](*data.get('args', []), **data.get('kwargs', {}))
            res = '' if res is None else res
            await websocket.send(json.dumps({'result': res}).encode())
        except ConnectionClosedError:
            # has a chance to prevent this from falling
            pass

    await websockets.serve(listener, "localhost", 9001)

async def main():
    await asyncio.gather(command_communicator(commands))
    await asyncio.sleep(0.1)
    
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    asyncio.get_event_loop().run_forever()
