import websockets
from websockets.exceptions import ConnectionClosedError
import json


async def command_communicator(commands):
    async def listener(websocket, path):
        try:
            jsoned = await websocket.recv()
            data = json.loads(jsoned.decode())
            print(data)
            msg = commands[data['command']](*data.get('args', []), **data.get('kwargs', {}))
            msg = '' if msg is None else msg
            await websocket.send(json.dumps({'msg': msg}).encode())
        except ConnectionClosedError:
            # has a chance to prevent this from falling
            pass

    await websockets.serve(listener, "localhost", 8766)
