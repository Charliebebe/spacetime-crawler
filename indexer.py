import json
import re
from bs4 import BeautifulSoup
import snowballstemmer
from collections import Counter
import math

# Dictionary where keys = indexes and values = tokens
forwardindex = {}

file = open("WEBPAGES_RAW/bookkeeping.json", "r")

#Dictionary that holds json formated data from file
book = json.load(file)

stemmer = snowballstemmer.stemmer('english')

# For every [directory, filename] pair in book.keys()
for localpath in book.keys():
    path = "WEBPAGES_RAW/" + localpath
    newfile = open(path, encoding="utf8")   # Open path
    readable = newfile.read().lower()
#    tokens = re.findall(r'[0-9a-z]+', readable)  # List of parsed tokens
    if '<html>' in readable:    # Ignore non HTML files
        soup = BeautifulSoup(readable, 'html.parser')
        forwardindex[path] = {}
        forwardindex[path]['normal'] = []
        forwardindex[path]['h1'] = []
        forwardindex[path]['h2'] = []
        forwardindex[path]['h3'] = []
        forwardindex[path]['h4'] = []
        forwardindex[path]['h5'] = []
        forwardindex[path]['h6'] = []
        forwardindex[path]['title'] = []

        for text in [el.text for el in soup.find_all('p')]:
            forwardindex[path]['normal'].extend(stemmer.stemWords(re.findall('[0-9a-z]+', text)))
        for text in [el.text for el in soup.find_all('span')]:
            forwardindex[path]['normal'].extend(stemmer.stemWords(re.findall('[0-9a-z]+', text)))
        for text in [el.text for el in soup.find_all('div')]:
            forwardindex[path]['normal'].extend(stemmer.stemWords(re.findall('[0-9a-z]+', text)))

        for text in [el.text for el in soup.find_all('h1')]:
            forwardindex[path]['h1'].extend(stemmer.stemWords(re.findall('[0-9a-z]+', text)))
        for text in [el.text for el in soup.find_all('h2')]:
            forwardindex[path]['h2'].extend(stemmer.stemWords(re.findall('[0-9a-z]+', text)))
        for text in [el.text for el in soup.find_all('h3')]:
            forwardindex[path]['h3'].extend(stemmer.stemWords(re.findall('[0-9a-z]+', text)))
        for text in [el.text for el in soup.find_all('h4')]:
            forwardindex[path]['h4'].extend(stemmer.stemWords(re.findall('[0-9a-z]+', text)))
        for text in [el.text for el in soup.find_all('h5')]:
            forwardindex[path]['h5'].extend(stemmer.stemWords(re.findall('[0-9a-z]+', text)))
        for text in [el.text for el in soup.find_all('h6')]:
            forwardindex[path]['h6'].extend(stemmer.stemWords(re.findall('[0-9a-z]+', text)))
        for text in [el.text for el in soup.find_all('title')]:
            forwardindex[path]['title'].extend(stemmer.stemWords(re.findall('[0-9a-z]+', text)))


inverted = {}


for path, termsdict in forwardindex.items():
    for tagelement, termlist in termsdict.items():
        for term in termlist:
            if term not in inverted:
                inverted[term] = Counter()  # {term: {doc: tf-idf weighted by tags}

                # Set tag scaled tf
                inverted[term][path] = \
                    forwardindex[path]['normal'].count(term) + \
                    forwardindex[path]['h1'].count(term)*2 + \
                    forwardindex[path]['h2'].count(term)*1.7 + \
                    forwardindex[path]['h3'].count(term)*1.6 + \
                    forwardindex[path]['h4'].count(term)*1.5 + \
                    forwardindex[path]['h5'].count(term)*1.4 + \
                    forwardindex[path]['h6'].count(term)*1.3 + \
                    forwardindex[path]['title'].count(term)*2

                inverted[term][path] = 1 + math.log10(inverted[term][path]) # Log tf

# Idf
for terms, docdict in inverted.items():
    for doc in docdict.keys():
        inverted[terms][doc] *= math.log10(len(forwardindex.keys() / len(docdict.keys())))


with open("invertedIndex.txt", "w") as f:
    for term, val in inverted.items():
        f.write('{} - '.format(term))
        for doc, score in val.items:
            f.write('{{ doc:{} score:{} }}, '.format(doc, score))
        f.write('\n')

print 'Written to file invertedIndex.txt\n'
print 'Number of documents: {}'.format(len(forwardindex.keys()))
print 'Number of unique words (stemmed): {}'.format(len(inverted.keys()))