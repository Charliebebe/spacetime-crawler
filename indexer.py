import json;
import re;
from bs4 import BeautifulSoup
from collections import Counter
import math
#Dictionary where keys = indexes and values = tokens
forwardindex = {}

file = open("WEBPAGES_RAW/bookkeeping.json", "r")

#Dictionary that holds json formated data from file
book = json.load(file)

#List of indexes after performing split
indexes = []

#Go through each key in dictionary book and split it on the "/" then append to indexes List
# for i in book.keys():
#     #Splits key into a list of [directory, filename] then appends it to indexes
#     x = i.split("/")
#     indexes.append(x)
#
# count = 0

#For every [directory,filename] in indexes
# while (count < len(indexes)):
#     # Create a deeper path
#     path = "WEBPAGES_RAW/" + indexes[count][0] + "/" + indexes[count][1]
#     newfile = open(path, encoding="utf8")
#     readable = newfile.read()
#     tokens = re.findall(r'[0-9a-z]+', readable)
#     forwardindex[indexes[count]] = tokens
#
#     count = count + 1

# For every [directory, filename] pair in book.keys()
for localpath in book.keys():
    path = "WEBPAGES_RAW/" + localpath
    newfile = open(path, encoding="utf8")   # Open path
    readable = newfile.read().lower()
    tokens = re.findall(r'[0-9a-z]+', readable)  # List of parsed tokens
    if '<html>' not in readable:
        forwardindex[path] = {}
        forwardindex[path]['p'] = tokens
        forwardindex[path]['h1'] = ''
        forwardindex[path]['h2'] = ''
        forwardindex[path]['h3'] = ''
        forwardindex[path]['h4'] = ''
        forwardindex[path]['h5'] = ''
        forwardindex[path]['h6'] = ''
    else:
        soup = BeautifulSoup(readable, 'lmxl')
        forwardindex[path] = {}
        forwardindex[path]['p'] = re.findall('[0-9a-z]+', soup.find('p').text)
        forwardindex[path]['h1'] = re.findall('[0-9a-z]+', soup.find('h1').text)
        forwardindex[path]['h2'] = re.findall('[0-9a-z]+', soup.find('h2').text)
        forwardindex[path]['h3'] = re.findall('[0-9a-z]+', soup.find('h3').text)
        forwardindex[path]['h4'] = re.findall('[0-9a-z]+', soup.find('h4').text)
        forwardindex[path]['h5'] = re.findall('[0-9a-z]+', soup.find('h5').text)
        forwardindex[path]['h6'] = re.findall('[0-9a-z]+', soup.find('h6').text)

inverted = {}


for path, termsdict in forwardindex.items():
    for tagelement, termlist in termsdict.items():
        for term in termlist:
            if term not in inverted:
                inverted[term] = Counter()  # {term: {doc: tf-idf weighted by tags}

                # Set tag scaled tf
                inverted[term][path] = \
                    forwardindex[path]['p'].count(term) + \
                    forwardindex[path]['h1'].count(term)*2 + \
                    forwardindex[path]['h2'].count(term)*1.9 + \
                    forwardindex[path]['h3'].count(term)*1.8 + \
                    forwardindex[path]['h4'].count(term)*1.7 + \
                    forwardindex[path]['h5'].count(term)*1.6 + \
                    forwardindex[path]['h6'].count(term)*1.5

                inverted[term][path] = 1 + math.log10(inverted[term][path])


for terms, docdict in inverted.items():
    for doc in docdict.keys():
        inverted[terms][doc] *= math.log10(len(forwardindex.keys() / len(docdict.keys())))

# print(indexes)
# print(book.values())