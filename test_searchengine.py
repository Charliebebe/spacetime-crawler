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
from sklearn.metrics.pairwise import linear_kernel
import numpy as np
import ast
from sklearn.metrics.pairwise import linear_kernel
import cPickle

stemmer = snowballstemmer.stemmer('english')

# Load index mappings to documents
corpus = json.load(io.open("corpus.json", "r"))
corpus = ast.literal_eval(corpus)

# Load fitted tfidf-matrix
# tfidf_matrix = json.load(io.open("tfidf_matrix.json", "r"))
# tfidf_matrix = ast.literal_eval(tfidf_matrix)['data']

tfidf_matrix = cPickle.load(open("tfidf_matrix.pickle", "rb"))


# Load trained tfidf-vectorizer
vectorizer = cPickle.load(open("vectorizer.pickle", "rb"))

# MAIN QUERY
query = "mondego"
query = " ".join(stemmer.stemWords(re.findall(r'[0-9a-z]+', query)))

# Calculate cosine similarity, return top document indices
query = vectorizer.transform([query])
cosine_similarities = linear_kernel(query, tfidf_matrix).flatten()
related_docs_indices = cosine_similarities.argsort()[:-5:-1]

print(related_docs_indices)
print(cosine_similarities[related_docs_indices])
print([corpus[index][0] for index in related_docs_indices])
# corpus[index][0] for doc link, corpus[index][1] for doc content


def query(textquery):
    textquery = ' '.join(stemmer.stemWords(re.findall(r'[0-9a-z]+', textquery)))
    textquerytfidf = vectorizer.transform([textquery])
    cosine_similarities = linear_kernel(textquerytfidf, tfidf_matrix).flatten()
    related_docs_indices = cosine_similarities.argsort()[:-5:-1]
