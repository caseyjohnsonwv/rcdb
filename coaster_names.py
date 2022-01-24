import requests
import re

class NameList:
    def __init__(self, max_count):
        self.max_count = max_count
        self.entries = [""]*max_count
        self.shortest = 0
    def add(self, name):
        if len(name) >= self.shortest:
            self.entries.append(name)
            self.entries.sort(key=len, reverse=True)
            self.entries = self.entries[:self.max_count]
            self.shortest = len(self.entries[self.max_count-1])
    def add_all(self, names):
        for n in names:
            self.add(n)
    def __repr__(self):
        return '\n'.join([f"{i+1}.) {name} ({len(name)})" for i,name in enumerate(self.entries)])

num = 25
longest = NameList(num)

table_data_pattern = re.compile('<td><a[^>]*>([^<]+)<\/a>(?:<td><a[^>]*>[^<]+<\/a>)+')
headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0'}
for page in range(1, 455):
    print(f"Querying page {page} of roller coasters...")
    url = f"http://rcdb.com/r.htm?ot=2&page={page}" # roller coasters in the world sorted by name
    r = requests.get(url, headers=headers)
    assert r.status_code == 200
    names = table_data_pattern.findall(r.text)
    longest.add_all(names)

print(f"{num} Longest Coaster Names:\n{longest}")