#!/home/photon/miniconda3/envs/robotics/bin/python


# if port is taken, run this:
# fuser -k 9001/tcp

from dataclasses import dataclass
import json
import os
import asyncio

import websockets
from websockets.exceptions import ConnectionClosedError
import numpy as np

import DobotDllType as dT
os.environ["LD_LIBRARY_PATH"] = ":/usr/DobotDllOutput"


@dataclass
class Dobot:
    j4_fixed: bool = True
    api: dT.CDLL = None
    addr: str = "192.168.225.186"
     
    def __post_init__(self):
        self.api = dT.load()
        self.connect()
        
    def connect(self):
        connected = not dT.ConnectDobot(self.api, self.addr, 115200)[0]
        if not connected:
            raise RuntimeError("couldt't connect")
        print("potentialy connected, sending init commands..."
              "(if hasn't printed 'ready' in several seconds, then restart)")
              
        dT.SetQueuedCmdClear(self.api)
        dT.SetHOMEParams(self.api, 200, 200, 200, 200, isQueued = 1)
        dT.SetCPParams(self.api, *dT.GetCPParams(self.api)[:3], 1)
        print("ready!")
        print(self.xyz)
    
    def disconnect(self):
        dT.DisconnectDobot(self.api)
    
    def __del__(self):
        self.disconnect()
    
    @property
    def pos(self):
        return dT.GetPose(self.api)
    
    @property
    def xyz(self):
        return self.pos[:3]
    
    @property
    def j4(self):
        if self.j4_fixed:
            return 0
        return self.pos[3]
    
    def move_to(self, xyzj):
        """
        xyzj can also be xyz (i. e. of length 3)
        """
        x, y, z = xyzj[:3]
        if len(xyzj) == 3:
            j4_rot = self.j4
        else:
            j4_rot = xyzj[3]
        dT.SetPTPCmd(self.api,
                     dT.PTPMode.PTPMOVLXYZMode,
                     x, y, z, j4_rot,
                     isQueued = 1)
    
    def move_delta(self, x: float = 0, y: float = 0, z: float = 0, j: float = 0):
        dT.SetCP2Cmd(self.api, 0, x, y, z, isQueued=1)
        # self.move_to(np.array(self.pos[:4]) + np.array([x, y, z, j]))



async def command_communicator(dobot):
    async def listener(websocket, path):
        try:
            jsoned = await websocket.recv()
            data = json.loads(jsoned)
            print(data)
            command, args, kwargs = data['command'], data.get('args', []), data.get('kwargs', {})
            
            func = getattr(dobot, command)
            if any([args, kwargs]):
                res = func(*args, **kwargs)
            else:
                res = func
            res = '' if res is None else res
            
            await websocket.send(json.dumps({'result': res}).encode())
        except ConnectionClosedError:
            # has a chance to prevent this from falling
            pass

    await websockets.serve(listener, "localhost", 9001)

async def main():
    await asyncio.gather(command_communicator(Dobot()))
    await asyncio.sleep(0.1)
    
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    asyncio.get_event_loop().run_forever()
