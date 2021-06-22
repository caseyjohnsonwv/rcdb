import csv
import re

text_file = 'park_coordinates.txt'
csv_file = 'park_coordinates.csv'

line_format_pattern = re.compile('(.+):\s+\((.+),(.+)\)')

with open(text_file, 'r') as input:
    data = input.readlines()
    with open(csv_file, 'w', newline='') as output:
        csvwriter = csv.writer(output)
        for d in data:
            m = line_format_pattern.match(d)
            park_name = m.group(1)
            park_latitude = float(m.group(2))
            park_longitude = float(m.group(3))
            row = [park_name, park_latitude, park_longitude]
            csvwriter.writerow(row)
