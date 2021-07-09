# QUESTION 5

# Decision tree learning
#
# Assumes discrete features. Examples may be inconsistent. Stopping condition for tree
# generation is when all examples have the same class, or there are no more features
# to split on (in which case, use the majority class). If a split yields no examples
# for a particular feature value, then the classification is based on the parent's
# majority class.

import math
import numpy as np
import matplotlib.pyplot as plt
import random
from google.colab import drive
drive.mount('/content/gdrive')

class TreeNode:
    def __init__(self, majClass):
        self.split_feature = -1 # -1 indicates leaf node
        self.children = {} # dictionary of {feature_value: child_tree_node}
        self.majority_class = majClass

#Function will split list up into a hardcoded 2 bins and will return the boundary 
def EqualFrequencyBinning(l):
    split = math.floor(len(l)/2)
    return l[split]

#Function will convert the continuous valued features into discrete features using equal frequency binning
def discretize(examples):
    discretized_list = examples.tolist()
    for feature_index in range(len(discretized_list[0]) - 1):
        boundary = EqualFrequencyBinning(sorted(examples[:,feature_index]))
        for example in discretized_list:
            if example[feature_index] > boundary :
                example[feature_index] = "> " + str(boundary)
            elif example[feature_index] <= boundary:
                example[feature_index] = "<= " + str(boundary)
    return discretized_list
  
def build_tree(examples):
    if not examples:
        return None
    # collect sets of values for each feature index, based on the examples
    features = {}
    for feature_index in range(len(examples[0]) - 1):
        features[feature_index] = set([example[feature_index] for example in examples])
    return build_tree_1(examples, features)
    
def build_tree_1(examples, features):
    tree_node = TreeNode(majority_class(examples))
    # if examples all have same class, then return leaf node predicting this class
    if same_class(examples):
        return tree_node
    # if no more features to split on, then return leaf node predicting majority class
    if not features:
        return tree_node
    # split on best feature and recursively generate children
    best_feature_index = best_feature(features, examples)
    tree_node.split_feature = best_feature_index
    remaining_features = features.copy()
    remaining_features.pop(best_feature_index)
    for feature_value in features[best_feature_index]:
        split_examples = filter_examples(examples, best_feature_index, feature_value)
        tree_node.children[feature_value] = build_tree_1(split_examples, remaining_features)
    return tree_node

def majority_class(examples):
    classes = [example[-1] for example in examples]
    return max(set(classes), key = classes.count)

def same_class(examples):
    classes = [example[-1] for example in examples]
    return (len(set(classes)) == 1)

def best_feature(features, examples):
    # Return index of feature with lowest entropy after split
    best_feature_index = -1
    best_entropy = 2.0 # max entropy = 1.0
    for feature_index in features:
        se = split_entropy(feature_index, features, examples)
        if se < best_entropy:
            best_entropy = se
            best_feature_index = feature_index
    return best_feature_index

def split_entropy(feature_index, features, examples):
    # Return weighted sum of entropy of each subset of examples by feature value.
    se = 0.0
    for feature_value in features[feature_index]:
        split_examples = filter_examples(examples, feature_index, feature_value)
        se += (float(len(split_examples)) / float(len(examples))) * entropy(split_examples)
    return se

def entropy(examples):
    classes = [example[-1] for example in examples]
    classes_set = set(classes)
    class_counts = [classes.count(c) for c in classes_set]
    e = 0.0
    class_sum = sum(class_counts)
    for class_count in class_counts:
        if class_count > 0:
            class_frac = float(class_count) / float(class_sum)
            e += (-1.0)* class_frac * math.log(class_frac, 2.0)
    return e

def filter_examples(examples, feature_index, feature_value):
    # Return subset of examples with given value for given feature index.
    return list(filter(lambda example: example[feature_index] == feature_value, examples))

def print_tree(tree_node, feature_names, depth = 1):
    indent_space = depth * "  "
    if tree_node.split_feature == -1: # leaf node
        print(indent_space + feature_names[-1] + ": " + tree_node.majority_class)
    else:
        for feature_value in tree_node.children:
            print(indent_space + feature_names[tree_node.split_feature] + " == " + feature_value)
            child_node = tree_node.children[feature_value]
            if child_node:
                print_tree(child_node, feature_names, depth+1)
            else:
                # no child node for this value, so use majority class of parent (tree_node)
                print(indent_space + "  " + feature_names[-1] + ": " + tree_node.majority_class)

def classify(tree_node, instance):
    if tree_node.split_feature == -1:
        return tree_node.majority_class
    child_node = tree_node.children[instance[tree_node.split_feature]]
    if child_node:
        return classify(child_node, instance)
    else:
        return tree_node.majority_class

#function picks random points from the dataset for training and testing
def random_subset(dataset, setsize):
  set_length = len(dataset) - 1
  subset = []
  for i in range(setsize):
    subset.append(dataset[random.randint(0, set_length)])
  return subset

#function that tests and returns the accuracy
def testing(tree, testsize, testdata):
  total = testsize
  correct = 0
  for i in range(testsize):
    temp = classify(tree, testdata[i])
    if temp == testdata[i][-1]:
      correct = correct + 1
  return float(correct) / float(total)

if __name__ == "__main__":
   feature_names = ["Color", "Type", "Origin", "Stolen"]
   
   examples = [
       ["Red", "Sports", "Domestic", "Yes"],
       ["Red", "Sports", "Domestic", "No"],
       ["Red", "Sports", "Domestic", "Yes"],
       ["Yellow", "Sports", "Domestic", "No"],
       ["Yellow", "Sports", "Imported", "Yes"],
       ["Yellow", "SUV", "Imported", "No"],
       ["Yellow", "SUV", "Imported", "Yes"],
       ["Yellow", "SUV", "Domestic", "No"],
       ["Red", "SUV", "Imported", "No"],
       ["Red", "Sports", "Imported", "Yes"]
       ]
   tree = build_tree(examples)
   print("Tree:")
   print_tree(tree, feature_names)
   test_instance = ["Red", "SUV", "Domestic"]
   test_class = classify(tree, test_instance)
   print("\nTest instance: " + str(test_instance))
   print("  class = " + test_class)
   
   #Loading the data
   data = np.loadtxt(fname="/content/gdrive/My Drive/ML/alldata.csv",delimiter=",")
   #Converting the continuous valued features into discrete features
   print("\n1.Converting continuous valued features into discrete features")
   test = discretize(data)
   print("Done")
   print("\n2.Training and testing with given dataset (100 random subset points for training, 80 random subset points for testing)")
   print("TRAINING....")
   #Training and testing the data
   t = build_tree(random_subset(test, 100))
   print("TESTING....")
   print("Accuracy : ", testing(t,80,random_subset(test,80)))
   print("Done")

   print("\n3.Training, testing and plotting points on the graph...")
   x = []
   y = []

   for i in range(10):
    size = 50 + (i * 200)
    temp = build_tree(random_subset(test, size))
    avg = 0
    #10 trials and taking the average of the 10 trials as the point
    for j in range(10):
      accuracy = testing(temp ,100,random_subset(test,100))
      avg = avg + accuracy
    x.append(size)
    y.append(avg/10)

   print("Training Instance (X - value): ", x)
   print("Testing Accuracy (Y - value): ", y)
   plt.plot(x,y,"bo-")