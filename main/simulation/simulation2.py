import os
import sys

#####incomplete######

# getting proper traci import
if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
import traci

# path to start sumo-gui
sumoBinary = '/opt/homebrew/bin/sumo-gui'
traci.start([sumoBinary, "-c", "osm.sumocfg"])

stats = dict()
# dict of dict
# key: vehicle_id,
# value: new diet:
    # 'departure_step' : _
    # 'arrival_step : _
    # 'route' : _
    # 'distance : _

# step = second
# this will run the simulation for an hour
for step in range(3600):
    print("step", step)
    
    # keep track of departures
    departed = list(traci.simulation.getDepartedIDList())
    if len(departed) != 0 :
        print("departed: ", end="")
        for d in departed:
            # exclude motor cycles
            if 'moto' not in d:
                print(d + " ", end="")
                stats[d] = dict()
                stats[d]['departure_step'] = step
                stats[d]['route'] = traci.vehicle.getRoute(d)
        print("")
    
    # when a vehicle arrives, calculate total distance
    arrived = traci.simulation.getArrivedIDList()
    if len(arrived) != 0 :
        print("arrived: ", end="")
        for a in arrived:
            # exclude motor cycles
            if 'moto' not in a:
                print(a + " ", end="")
                stats[a]['arrival_step'] = step

                for edge in stats[a]['route']:
                    traci.subscribe

        print("")
    
    # move forward one step
    traci.simulationStep()

# don't wait for program to close to finish script execution.
traci.close(False)

from datetime import datetime
current_date_time = datetime.now().strftime("%m%d%Y-%H:%M")

# save as csv
import csv
with open('testing' + current_date_time + ".csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['vehicle_id', 'total_seconds', 'total_distance'])
    for vehicle_id, s in stats.items():
        time = s['arrival_step'] - s['departure_step']
        writer.writerow(vehicle_id, time, s['distance'])

