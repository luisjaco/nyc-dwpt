import os
import sys

if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))

import traci

sumoBinary = '/opt/homebrew/bin/sumo-gui'

traci.start([sumoBinary, "-c", "osm.sumocfg"])

departures = dict()
times = dict()
# step = second

# this will run the simulation for an hour
for step in range(36):
    print("step", step)
    
    departed = list(traci.simulation.getDepartedIDList())
    if len(departed) != 0 :
        print("departed: ", end="")
        for d in departed:
            print(d + " ", end="")
            departures[d] = step
        print("")
    
    arrived = traci.simulation.getArrivedIDList()
    if len(arrived) != 0 :
        print("arrived: ", end="")
        for a in arrived:
            print(a + " ", end="")
            times[a] = step - departures[a]
        print("")
    
    traci.simulationStep()

# don't wait for program to close.
traci.close(False)

from datetime import datetime

current_date_time = datetime.now().strftime("%m%d%Y-%H:%M")
# save as csv
import csv
with open('all_density' + current_date_time + ".csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['vehicle_id', 'total_seconds'])
    for vehicle_id, time in times.items():
        if 'moto' not in vehicle_id: # don't want motorcycles
            writer.writerow([vehicle_id, time])
