import json
import re
from bs4 import BeautifulSoup
import snowballstemmer
import nltk
from collections import Counter
import math
import io
import string
from sklearn.feature_extraction.text import TfidfVectorizer
# Dictionary where keys = indexes and values = tokens


file = io.open("WEBPAGES_RAW/bookkeeping.json", "r")



#Dictionary that holds json formated data from file
book = json.load(file)
corpus = {}
count = 0
stemmer = snowballstemmer.stemmer('english')


for localpath, link in book.items():
    path = "WEBPAGES_RAW/" + localpath
    newfile = io.open(path, encoding="utf8")   # Open path
    readable = newfile.read().lower()
    if '</html>' in readable:
        soup = BeautifulSoup(readable, 'html.parser')
        # for el in soup.find_all('p'):
        #     doc= ' '.join([doc, ' '.join(stemmer.stemWords(re.findall(r'[0-9a-z]+', el.text)))])

        doc = ' '.join([' '.join(stemmer.stemWords(re.findall(r'[0-9a-z]+', el.text))) for el in soup.find_all('p')])
        corpus[count] = (link, doc)
    else:
        corpus[count] = (link, '')
    count = count + 1


vectorizer = TfidfVectorizer(stop_words='english',min_df=1,lowercase=True, sublinear_tf=True)
c = [value[1] for value in corpus.values()]
X = vectorizer.fit_transform(c)
import numpy
numpy.set_printoptions(threshold=numpy.nan)

inverted = {}
feature_names = vectorizer.get_feature_names()
row,col = numpy.nonzero(X.T)
for x,y in zip(row, col):
    if feature_names[x] not in inverted:
        inverted[feature_names[x]] = []
    inverted[feature_names[x]].append({corpus[y][0]: X[y,x]})
    # print (feature_names[x], corpus[y][0],  X[y,x])
# print(vectorizer.get_feature_names())
# print (corpus)
# print (inverted['irvin'])

with io.open('inverted_index.json', 'w', encoding='utf-8') as json_file:
    json.dump(unicode(inverted), json_file, ensure_ascii=False, indent=4)

print ('Written to file inverted_index.json\n')
print ('Number of documents: ', X.shape[0])
print ('Number of unique words: ', X.shape[1])