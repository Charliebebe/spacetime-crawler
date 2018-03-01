import json;
import re;

forwardindex = {}
file = open("WEBPAGES_RAW/bookkeeping.json", "r")
book = json.load(file)
indexes = []
sites = []
for i in book.keys():
    x = i.split("/")
    indexes.append(x)

for i in book.values():
    sites.append(i)

count = 0

while (count < len(sites)):
    path = "WEBPAGES_RAW/" + indexes[count][0] + "/" + indexes[count][1]
    newfile = open(path, encoding="utf8")
    readable = newfile.read()
    tokens = re.findall(r'[0-9a-z]+', readable)
    forwardindex[indexes[count]] = tokens

    count = count + 1

inverted = {}

for key,value in forwardindex.items():
    for i in value:
        if i in inverted:
            if key in inverted[i]:
                continue;
            else:
                inverted[i].append(key)
        else:
            inverted[i] = [key]
# print(indexes)
# print(book.values())