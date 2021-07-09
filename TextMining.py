#https://colab.research.google.com/drive/19vlayGa3UVXlfplChsL3YWr4V8OqNBgm?usp=sharing

# https://scikit-learn.org/0.19/datasets/twenty_newsgroups.html
from sklearn.datasets import fetch_20newsgroups

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction import stop_words
from nltk.tokenize import TreebankWordTokenizer

import numpy as np
import pandas as pd
import pprint

# We will work with 12 of the 20 categories
categories = ['rec.autos', 'rec.motorcycles', 'rec.sport.baseball', \
              'rec.sport.hockey', 'sci.med', 'sci.space', 'sci.electronics', \
              'comp.graphics', 'comp.windows.x', 'talk.religion.misc', \
              'talk.politics.mideast', 'talk.politics.misc']
newsgroups = fetch_20newsgroups(categories=categories)

print('List of newsgroup categories:')
print(list(newsgroups.target_names))
print("\n")


# print first line of the first data file as a sample
"""
print('Sample file')
print("\n".join(newsgroups.data[2].split("\n")[:10]))
print("\n")
print('data', newsgroups.data[2])
"""

# convert collection of documents to matrix of string (word) counts
count_vect = CountVectorizer()

# use regular expressions to convert text to tokens
# split contractions, separate punctuation
tokenizer = TreebankWordTokenizer()
count_vect.set_params(tokenizer=tokenizer.tokenize)

# remove English stop words (try with and without this)
#count_vect.set_params(stop_words='english')
#print(stop_words.ENGLISH_STOP_WORDS)

# include 1-grams and 2-grams
#count_vect.set_params(ngram_range=(1,2))

# ignore terms that appear in >50% of the documents, try with and without this
#count_vect.set_params(max_df=0.5)

# ignore terms that appear in only 1 document, try with and without this
#count_vect.set_params(min_df=2)

# transform text to bag of words vector using parameters
X_counts = count_vect.fit_transform(newsgroups.data)

# normalize counts based on document length
# weight common words less (is, a, an, the)
tfidf_transformer = TfidfTransformer()
X_tfidf = tfidf_transformer.fit_transform(X_counts)

# train a naive Bayes classifier on data, multinomial for discrete features
clf = MultinomialNB().fit(X_tfidf, newsgroups.target)
scores = cross_val_score(clf, X_tfidf, newsgroups.target, cv=3, \
                         scoring='accuracy')
print('Number of documents:', len(newsgroups.target), ', 3-fold accuracy:', np.mean(scores))


def detailed_report():
  X_train, X_test, y_train, y_test = train_test_split(X_tfidf, newsgroups.target, test_size = 0.33)
  clf.fit(X_train, y_train)
  y_pred = clf.predict(X_test)

  #y_true_labels = list(map(lambda x: newsgroups.target_names[x], y_test))
  #y_pred_labels = list(map(lambda x: newsgroups.target_names[x], y_pred))

  # confusion matrix, show first time
  print('Confusion matrix:')
  pprint.pprint(newsgroups.target_names, width=200)
  print(confusion_matrix(y_test, y_pred))