# this is a set of the edges (streets) for
# east 42nd street and west 42nd street.
# refer to get_edges.py to alter this list

target_edges = set(['-1136952921#1', '-1272613980#2', '-1272613981#1', '-1320232776#1', '-1320290376#1', '-1320549615#1', '-1321771943#2', '-167922072#1', '-167922076#2', '-167922077#1', '-169267538#1', '-384826723#2', '-420356168#4', '-420356169#3', '-420904618#3', '-420904620', '-420904621#1', '-511699183#2', '-525729008#5', '-542259076#3', '-5672991#5', '-68325079#1', '-747908051#1', '-747908052#2', '-988980354#1', '-989265269#1', '1136952921#0', '1272613980#0', '1320232776#0', '1320290376#0', '1320549615#0', '1321771943#0', '1364312922', '167922072#0', '167922076#0', '167922077#0', '169267538#0', '384826723#0', '420356168#0', '420356169#0', '420904618#0', '420904620', '420904621#0', '438384692#0', '46201630#0', '46201630#0-AddedOffRampEdge', '511699183#0', '525729008#0', '542259076#0', '747908052#0', '747908053', '974611019#0', '988980354#0', '989265269#0'])
# main simulation:

import os
import sys

if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))

import traci

# [!] change to sumo-gui to open the gui
sumoBinary = '/opt/homebrew/bin/sumo'

# steps/seconds are measured in simulation time, not real time. 
# time is dependent on the speed of the simulation, which can be influenced by traffic density,
# speed limits, roads, etc.

scale = "1.35" # traffic scale; 1.35 is a medium traffic scenario
beginning = 0 # this value will be > 0 if you want a delay before trips are tracked; in seconds (steps)
duration = float('inf') # when a simulation should end; in seconds (steps)

# start with traffic scale set to 1.35 (medium-traffic scenario)
traci.start([sumoBinary, "-c", "osm.sumocfg", "--scale", scale])

# entry_times = {}
# durations = {}
# step = second

entries = {}
totals = {}

step = 0

while step < beginning:
    print("step", step)
    traci.simulationStep()
    step += 1

print("starting to count")
# this will run the simulation for two hours
while traci.simulation.getMinExpectedNumber() > 0 and step < duration:
    print(step)

    for vehID in traci.vehicle.getIDList():
        current_edge = traci.vehicle.getRoadID(vehID)

        if current_edge in target_edges:
            if vehID not in entries:
                entries[vehID] = step

        # if vehicle had an entry but not longer in the edge, they left.
        elif vehID in entries: 
            if vehID not in totals:
                totals[vehID] = step - entries[vehID] # current step - entry = time spent
            else:
                totals[vehID] += step - entries[vehID]
            # remove entry, in case it comes back
            entries.pop(vehID)

        # if car is in desired edge
        # if current_edge in target_edges:
        #     if vehID not in total_times:
        #         total_times[vehID] = 1
        #     else: # vehicle already there, add one
        #         total_times[vehID] += 1

            # if vehID not in entry_times:
            #     entry_times[vehID] = step
            #     print(vehID, "added to entry times")
            # else:
            #     # vehicle exited
            #     if vehID in entry_times:
            #         print(vehID, "updated duration")
            #         time_spent = step - entry_times[vehID]
            #         durations[vehID] = durations.get(vehID, 0) + time_spent

    traci.simulationStep()
    step += 1

# don't wait for program to close.
traci.close(False)

# create file to analyze
from datetime import datetime

current_date_time = datetime.now().strftime("%m%d%Y-%H:%M")
# save as csv
import csv
with open('nyc_42nd_st_' + current_date_time + ".csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['vehicle_id', 'total_seconds'])
    for vehicle_id, time in totals.items():
        writer.writerow([vehicle_id, time])
