# in this file, we will find the names of the edge ids which
# have the street name "East 42nd Street" or "West 42nd Street".
# im not gonna lie i chatgptd this

import os
import sys

if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))

from sumolib import net

netfile = "osm.net.xml"  # path to your network file
net = net.readNet(netfile)

# Find all edges with name "42nd Street"
edges_42nd = [
    edge.getID() for edge in net.getEdges() if edge.getName() == "West 42nd Street" or edge.getName() == "East 42nd Street"
    ]

print("42nd Street:", edges_42nd)
