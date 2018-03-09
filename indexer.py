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
print (inverted['irvin'])

with io.open('inverted_index.json', 'w', encoding='utf-8') as json_file:
    json.dump(inverted, json_file, ensure_ascii=False)

print ('Written to file inverted_index.json\n')

# for key,val in corpus.items():
#     X = vectorizer.transform([val])
#     doctermidf = [{}]
#     for col in X.nonzero()[1]:
#
#         print (feature_names[col], ' - ', X[0, col])

    # print(feature_names[X[0][1]], " - ", X[1])
# for col, termrow in enumerate(X.T):
#     print (feature_names[col], ' - '),
#     for doc in termrow:
#         print (doc),
#     print ('\n')

# str = ['univ of waterloo', 'machin']
# print (str)
# response = vectorizer.transform(str)
# print (response)
# print (feature_names[959], feature_names[932], feature_names[574])
# for col in X.nonzero()[1]:
#     print (feature_names[col], ' - ', X[0, col])
# print (X.shape)
# idf = vectorizer.idf_
# print(vectorizer.get_feature_names(), idf)
#
#
# idf = vectorizer.idf_
# inverted_index = dict(zip(vectorizer.get_feature_names(), idf))
# print (inverted_index)
"""


# For every [directory, filename] pair in book.keys()
for localpath in book.keys():
    path = "WEBPAGES_RAW/" + localpath
    newfile = io.open(path, encoding="utf8")   # Open path
    readable = newfile.read().lower()
#    tokens = re.findall(r'[0-9a-z]+', readable)  # List of parsed tokens
    if '<html>' in readable:    # Ignore non HTML files
        
        forwardindex[path] = {}
        forwardindex[path]['normal'] = []
        forwardindex[path]['h1'] = []
        forwardindex[path]['h2'] = []
        forwardindex[path]['h3'] = []
        forwardindex[path]['h4'] = []
        forwardindex[path]['h5'] = []
        forwardindex[path]['h6'] = []
        forwardindex[path]['title'] = []

        for el in soup.find_all('p'):
            forwardindex[path]['normal'].extend(stemmer.stemWords(re.findall('[0-9a-z]+', el.text)))
        for el in soup.find_all('span'):
            forwardindex[path]['normal'].extend(stemmer.stemWords(re.findall('[0-9a-z]+', el.text)))
        for el in soup.find_all('div'):
            forwardindex[path]['normal'].extend(stemmer.stemWords(re.findall('[0-9a-z]+', el.text)))

        for el in soup.find_all('h1'):
            forwardindex[path]['h1'].extend(stemmer.stemWords(re.findall('[0-9a-z]+', el.text)))
        for el in soup.find_all('h2'):
            forwardindex[path]['h2'].extend(stemmer.stemWords(re.findall('[0-9a-z]+', el.text)))
        for el in soup.find_all('h3'):
            forwardindex[path]['h3'].extend(stemmer.stemWords(re.findall('[0-9a-z]+', el.text)))
        for el in soup.find_all('h4'):
            forwardindex[path]['h4'].extend(stemmer.stemWords(re.findall('[0-9a-z]+', el.text)))
        for el in soup.find_all('h5'):
            forwardindex[path]['h5'].extend(stemmer.stemWords(re.findall('[0-9a-z]+', el.text)))
        for el in soup.find_all('h6'):
            forwardindex[path]['h6'].extend(stemmer.stemWords(re.findall('[0-9a-z]+', el.text)))
        for el in soup.find_all('title'):
            forwardindex[path]['title'].extend(stemmer.stemWords(re.findall('[0-9a-z]+', el.text)))


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

                # Log-tf, divided by total tf in that document
                inverted[term][path] = 1 + math.log10(inverted[term][path] / \
                                                      (len(forwardindex[path]['normal']) + \
                                                       len(forwardindex[path]['h1']) + \
                                                       len(forwardindex[path]['h2']) + \
                                                       len(forwardindex[path]['h3']) + \
                                                       len(forwardindex[path]['h4']) + \
                                                       len(forwardindex[path]['h5']) + \
                                                       len(forwardindex[path]['h6']) + \
                                                       len(forwardindex[path]['title']))) # Log tf

# Idf normalization
for terms, docdict in inverted.items():
    for doc in docdict.keys():
        inverted[terms][doc] *= math.log10( len(forwardindex.keys()) / len(docdict.keys()) )


# with open("invertedIndex.txt", "w") as f:
#     for term, val in inverted.items():
#         f.write('{} - '.format(term))
#         for doc, score in val.items:
#             f.write('{{ doc:{} score:{} }}, '.format(doc, score))
#         f.write('\n')

inverted_index = []

# Create JSON formatted array with
# SCHEMA:
#   [   {   term: 'cat',
#           docs: [ {   docname: docname1,
#                       tf-idf: num },
#                   {   docname: docname2,
#                       tf-idf: num }]
#       },
#       {   term: 'dog',
#           docs: [ {   docname: docname1,
#                       tf-idf: num },
#                   {   docname: docname2,
#                       tf-idf: num }]
#       },]
for term, docs in inverted.items():
    dict = {}
    dict['term'] = term
    dict['docs'] = [{'doc': doc, 'tfidf': tfidf} for doc, tfidf in docs.items()]
    inverted_index.append(dict)

with io.open('inverted_index.json', 'w', encoding='utf-8') as json_file:
    json.dump(inverted_index, json_file, ensure_ascii=False)

print 'Written to file inverted_index.json\n'
print 'Number of documents: {}'.format(len(forwardindex.keys()))
print 'Number of unique words (stemmed): {}'.format(len(inverted.keys()))
"""