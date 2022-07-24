import sam_emitter
import json
import random
import string
import time
sam1 = sam_emitter.Sam_Emitter('sam01', 0, 0)

pos_report = {'id':0, \
                           'name':''.join(random.choices(string.ascii_uppercase, k=3)) + \
                                  ''.join(random.choices(string.digits, k=3)), \
                           'source':'simulated', \
                           'time':time.time(), \
                           'lat':-1.7, \
                           'lng':0.5, \
                           'alt':30000, \
                           'hdg':random.randrange(0,359), \
                           'gnd_spd':500 }

new_target = {"cur_target":pos_report['name'], "cur_threat":"spiffy_proposal"}
sam1.change_target(new_target)
for i in range(50):
    pos_report['time']=time.time()
    pos_report['lat']= pos_report['lat']+.05
    targets = []
    targets.append(pos_report)
    sam1.track_target(json.dumps(targets))
    print('sam el: {}\nsam az: {}\ntarget loc:\nlat {}, long {}'.format(sam1.get_status()['el'], sam1.get_status()['az'], pos_report['lat'], pos_report['lng']))
