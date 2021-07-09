import numpy as np
from sklearn.dummy import DummyClassifier
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn.model_selection import train_test_split
import math


# My implementation of KNN
class My_KNN:
  def __init__(self, k_neighbors):
    self.k_neighbors = k_neighbors
    self.X_train = [[]]
    self.y_train = []
  
  # Method calculates the euclidean distance
  def euclideanDistance(self, x, y):
    sum = 0
    for i in range(len(x) - 1):
      sum = sum + math.pow((x[i] - y[i]), 2)
    return math.sqrt(sum)
  
  # Method just sets the X_train and y_train since KNN has no training
  def fit(self, X_train, y_train):
    self.X_train = X_train
    self.y_train = y_train
  
  # Predicts the label for the x_test with the KNN Algorithm 
  def predict(self, X_test):
    newlabels = []
    X_test = X_test
    for x in X_test:
      S = []
      for n in self.X_train:
        S.append(self.euclideanDistance(x, n))
      # Sort the distances and return the indices of k neighbors
      D = np.argsort(S)[:self.k_neighbors]
      neighbors = {}
      for k in D:
        if self.y_train[k] in neighbors: 
          neighbors[self.y_train[k]] = neighbors[self.y_train[k]] + 1
        else:
          neighbors[self.y_train[k]] = 1
      newlabels.append(max(neighbors, key=neighbors.get)) #append the majority
    return newlabels

classifiers = [
    (DummyClassifier(strategy="most_frequent"),"Simple Majority"),
    (DecisionTreeClassifier(criterion="entropy"), "Decision Tree"),
    (KNeighborsClassifier(n_neighbors=1), "1NN"),
    (KNeighborsClassifier(n_neighbors=3), "3NN"),
    (KNeighborsClassifier(n_neighbors=5), "5NN"),
    (KNeighborsClassifier(n_neighbors=7), "7NN"),
    (KNeighborsClassifier(n_neighbors=9), "9NN"),
    (My_KNN(1), "MY 1NN"),
    (My_KNN(3), "MY 3NN"),
    (My_KNN(5), "MY 5NN"),
    (My_KNN(7), "MY 7NN"),
    (My_KNN(9), "MY 9NN")
]

def read_data():
    data = np.loadtxt(fname='alldata.csv',delimiter=',')
    X = data[:,:-1]
    y = data[:,-1]
    return X, y

def sklearn_majority_train(X, y):
    classifier = DummyClassifier(strategy="most_frequent")
    classifier.fit(X, y)
    return classifier

def sklearn_majority_test(classifier, X, y):
    newlabels = classifier.predict(x)
    print("accuracy is",metrics.accuracy_score(y, newlabels))
    print(metrics.confusion_matrix(y, newlabels))

X, y = read_data()


print("MY IMPLEMENTATION OF KNN IS A LITTLE SLOW!!!!\n")
for clf, name in classifiers:
    print("Classifier:", name)
    accuracy = 0.0
    for x in range(3):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
        clf.fit(X_train, y_train)
        newlabels = clf.predict(X_test)
        accuracy = accuracy + metrics.accuracy_score(y_test,newlabels)
    print("Accuracy:",accuracy/3,'\n')
