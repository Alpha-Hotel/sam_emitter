# Ingest module
#
# Gets position reports from any source and translates to a pos_report object, then output in json over a websocket
#
# Currently just generates a simulated target that flies in a straight line at a constant speed on a constant heading
# 

import json, time, math, sys, asyncio, random, string
import websockets as ws

print('sam-ingest: starting')

# simulated active target class
class sim_target:

    def __init__(self):
        
        self.pos_report = {'id':0, \
                           'name':''.join(random.choices(string.ascii_uppercase, k=3)) + \
                                  ''.join(random.choices(string.digits, k=3)), \
                           'source':'simulated', \
                           'time':time.time(), \
                           'lat':37.7, \
                           'lng':-76.5, \
                           'alt':20000, \
                           'hdg':random.randrange(0,359), \
                           'gnd_spd':500 }

        print('sam-ingest: sim target ' + self.pos_report['name'] + ' created')

    def update_position(self):
        # conversion factors:
        # degrees latitude to feet  = 364000
        # degrees longitude to feet = 288200
        # knots to feet per second  = 1.68781

        # bounds for aircraft
        #   
        # -77.46 W, 38.3 N (Fredericksburg, VA)  
        # -76 W, 37.3 N (Delmarva Peninsula)
        
        self.pos_report['time'] = time.time()

        #
        # If the aircraft reaches bounds, have him turn around.
        #
        
        # change heading if we go too far east or west
        if self.pos_report['lng'] < -77.4:
            # change heading to 030-150 randomly
            self.pos_report['hdg'] = random.randrange(30, 150, 1) 
        elif self.pos_report['lng'] > -76:
            #change heading to to 210-330
            self.pos_report['hdg'] = random.randrange(210, 330, 1)

        # change heading if we go too far north or south
        if self.pos_report['lat'] > 38.3:
            # change heading to 120-240
            self.pos_report['hdg'] = random.randrange(120, 240, 1)
        elif self.pos_report['lat'] < 37.3:
            # change heading to 300 - 60
            self.pos_report['hdg'] = random.randrange(300, 420, 1) % 360

        delta_lat = (self.pos_report['gnd_spd'] * 1.68781) * math.cos(math.radians(self.pos_report['hdg']))
        delta_lng = (self.pos_report['gnd_spd'] * 1.68781) * math.sin(math.radians(self.pos_report['hdg']))

        self.pos_report['lat'] = self.pos_report['lat'] + (delta_lat / 364000)
        self.pos_report['lng'] = self.pos_report['lng'] + (delta_lng / 288200)
        
        print('sam-ingest: updated position of ' + self.pos_report['name'])

    #async def output_json_ws(self):
    #    print('sam-ingest: sending position report ' + self.pos_report['name'])
    #    async with ws.connect('ws://localhost:8765') as websocket:
    #        await websocket.serve(vjson.dumps(self.pos_report, indent = 4))
    #        #ws_msg_ack = await websocket.recv()
    #        #print('sam-ingest: ' + ws_msg_ack)
            
#
# Create and  an aircraft
# This probably belongs somewhere else
#

# Create a simulated target
#test_tgt = sim_target()
# This should run for 10 minutes
#for tgt_update in range(0, 600):
#    asyncio.run(test_tgt.output_json_ws())
#    test_tgt.update_position()
#    time.sleep(1)

