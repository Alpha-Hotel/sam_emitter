#
# sam-wsclient connects to SAM and INGEST servers and recieves JSON objects
#

import websockets as ws

import asyncio, json, tkinter


async def recv_message(websocket, path):
    message_json = await websocket.recv()

    message = json.loads(message_json)
    print(message)

async def main_ingest():
    while True:
        async with ws.connect('ws://localhost:6969') as websocket:
            while True:
                message = await websocket.recv()
                print(message)
                await websocket.send('sam_wsclient: recieved aircraft')

async def main_sam_emitter():
    while True:
        async with ws.connect('ws://localhost:7060') as websocket:
            while True:
                message = await websocket.recv()
                print(message)
                await websocket.send('sam_wsclient: recieved emitter')

def sam_emitter_command():
    pass


wsclient_loop = asyncio.get_event_loop()

asyncio.ensure_future(main_ingest())
asyncio.ensure_future(main_sam_emitter())

wsclient_loop.run_forever()
