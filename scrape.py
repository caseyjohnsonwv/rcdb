import requests
import re

data_id_pattern = re.compile('href=\/(\d+)')
data_ids = []
for page in range(13, 17):
    print("Querying page {pg} of amusement parks...".format(pg=page))
    url = "https://rcdb.com/r.htm?st=93&ol=59&order=28&ot=3&page={pg}".format(pg=page) #amusement parks operating in the US sorted by number of coasters descending
    r = requests.get(url)
    data_ids.extend(data_id_pattern.findall(r.text))

park_coordinates_pattern = re.compile('destination=(-?[\d]+\.[\d]+),(-?[\d]+\.[\d]+)')
park_name_pattern = re.compile('<h1>(.+)</h1>')
park_coordinates = []
park_names = []
for data_id in data_ids:
    print("Querying park ID {id}...".format(id=data_id))
    url = "https://rcdb.com/{id}.htm".format(id=data_id)
    r = requests.get(url)
    try:
        name = park_name_pattern.findall(r.text)[0]
        park_names.append(name)
        print("Park ID {id} is {park_name}!".format(id=data_id, park_name=name))
    except:
        park_names.append(data_id)
        print("Could not find valid park name for {id}!".format(id=data_id))
    try:
        coords = park_coordinates_pattern.findall(r.text)[0]
        coords = (float(coords[0]), float(coords[1]))
        park_coordinates.append(coords)
    except:
        park_coordinates.append((0,0))
        print("Could not find valid coordinates for {id}!".format(id=data_id))

assert len(data_ids) == len(park_coordinates) == len(park_names)
output = {}
for i in range(len(park_names)):
    output[data_ids[i]] = {'name':park_names[i], 'coords':park_coordinates[i]}

output_file = 'park_coordinates.txt'
print("Writing parks & coordinates to {filename}...".format(filename=output_file))
with open(output_file, 'a') as f:
    for k,v in output.items():
        f.write("{name}: {coords}\n".format(name=v['name'], coords=v['coords']))
