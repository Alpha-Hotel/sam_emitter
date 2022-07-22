#!/usr/bin/python3

#
# sam emitter sim server
#

import asyncio, json, random

import websockets as ws

import sam_emitter

emitter_server_port = 7060
global current_acft_pos_repo

async def main():
    while True:
        await asyncio.sleep(1)

async def send_status_report(websocket, path):
    while True:
        emitter_status_json_list = []

        for i in range(0,3):
            emitter_status_json_list.append(sim_emitter_list[i].get_status())

        try:
            await websocket.send(json.dumps(emitter_status_json_list))
        except websockets.exceptions.ConnectionClosedOK:
            print('sam_emitter: client closed connection, not a problem')

        # get ack and handle if it's a command
        message = await websocket.recv()


        try:
            decoded_message = json.loads(message)
            print('sam_emitter_sim: recieved command for ' + decoded_message['sam_id'])
            [emitter for emitter in sim_emitter_list if emitter.name == decoded_message['sam_id']][0].change_target(decoded_message)

        except ValueError:
            print('sam_emitter_sim: recieved client response: ' + message)


        for i in range(0, len(sim_emitter_list)):
            sim_emitter_list[i].track_target(current_acft_pos_rep)
            pass


        await asyncio.sleep(1)


async def ingest_client_ws():
    while True:
        async with ws.connect('ws://localhost:6969') as websocket:
            while True:
                message_ingest = await websocket.recv()

                global current_acft_pos_rep
                current_acft_pos_rep = message_ingest
                await websocket.send('sam_emitter_sim: recieved')


sim_emitter_server = ws.serve(send_status_report, 'localhost', emitter_server_port)

sim_emitter_list = []

# create list containing emitter objects
for i in range(0,3):
    new_emitter_name = 'SAM00' + str(i)
    sim_emitter_list.append(sam_emitter.Sam_Emitter(new_emitter_name, random.randrange(3730, 3830, 1)/100, random.randrange(-7740, -7600, 1)/100))

asyncio.get_event_loop().run_until_complete(sim_emitter_server)
asyncio.get_event_loop().run_until_complete(ingest_client_ws())
asyncio.get_event_loop().run_until_complete(main())
asyncio.get_event_loop.run_forever()
