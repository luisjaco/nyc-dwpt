# will sort a .passenger.trips.xml file by departure
# you must have the file sorted by departure for it to accurately work

import xml.etree.ElementTree as ET


with open("/opt/homebrew/Cellar/sumo@1.9.2/1.9.2_2/share/sumo/tools/2025-05-07-12-41-55/resources/create_trips.xml") as f:
    print(f.readline())


# Input and output file paths
input_file = "/opt/homebrew/Cellar/sumo@1.9.2/1.9.2_2/share/sumo/tools/2025-05-07-12-41-55/resources/create_trips.xml"
output_file = "/opt/homebrew/Cellar/sumo@1.9.2/1.9.2_2/share/sumo/tools/2025-05-07-12-41-55/resources/sorted.passenger.trips.xml"

# Parse the input XML
tree = ET.parse(input_file)
root = tree.getroot()

# Extract <trip> elements
trips = root.findall('trip') + root.findall('vehicle')

# Sort trips by 'depart' attribute (as float)
sorted_trips = sorted(trips, key=lambda trip: float(trip.attrib['depart']))

# Remove original trips
for trip in trips:
    root.remove(trip)

# Append sorted trips
for trip in sorted_trips:
    root.append(trip)

# Write the sorted XML to a file
tree.write(output_file, encoding="UTF-8", xml_declaration=True)

print(f"Sorted trips saved to: {output_file}")