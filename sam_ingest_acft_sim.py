#
# sam ingest server
#

#import threading, asyncio, time

import asyncio, json

import websockets as ws

import sam_ingest

number_of_acft = 1
fake_acft_threads = []
ingest_server_port = 6969

# websockets server functions

async def main():
    while True:
        #sim_acft.update_position()

        for i in range(0, len(sim_acft_list), 1):
            sim_acft_list[i].update_position()

        await asyncio.sleep(1)

async def send_pos_report(websocket, path):
    while True:
        #await websocket.send(json.dumps(sim_acft.pos_report))
        #print(sim_acft_list)
        #await websocket.send(json.dumps(sim_acft_list))
        
        pos_rep_list = []

        for i in range(0, len(sim_acft_list), 1):
            pos_rep_list.append(sim_acft_list[i].pos_report)

        await websocket.send(json.dumps(pos_rep_list))

        print(await websocket.recv())
        await asyncio.sleep(1)

sim_ingest_server = ws.serve(send_pos_report, 'localhost', ingest_server_port)

#sim_acft = sam_ingest.sim_target()

sim_acft_list = []

for i in range(0, 3, 1):
    sim_acft_list.append(sam_ingest.sim_target())


asyncio.get_event_loop().run_until_complete(sim_ingest_server)
asyncio.get_event_loop().run_until_complete(main())
asyncio.get_event_loop().run_forever()

