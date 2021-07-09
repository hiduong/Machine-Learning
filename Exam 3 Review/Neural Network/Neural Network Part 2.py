from random import random
import numpy as np

def initialize_network(n_inputs, n_hidden, n_outputs):
    network = list() #initialize weights to random number in [0..1]
    hidden_layer = [{'weights':[random() for i in range(n_inputs+1)]} for i in range(n_hidden)]
    network.append(hidden_layer)
    output_layer = [{'weights':[random() for i in range(n_hidden+1)]} for i in range(n_outputs)]
    network.append(output_layer)
    return network

def activate(weights, inputs):
    activation = weights[-1] # bias weight
    for i in range(len(weights)-1):
        activation += weights[i] * inputs[i]
    return activation

def transfer(activation):
    return np.tanh(activation)

def forward_propagate(network, row):
    inputs = row
    for layer in network:
        new_inputs = []
        for node in layer:
            activation = activate(node['weights'], inputs)
            node['output'] = transfer(activation)
            new_inputs.append(node['output']) # output of one node input to another
        inputs = new_inputs
    return inputs # return output from last layer

def transfer_derivative(output):
    return 1.0 - np.tanh(output)**2

def backward_propagate_error(network, expected):
    for i in reversed(range(len(network))): # from output back to input layers
        layer = network[i]
        errors = list()
        if i != len(network)-1: # not the output layer
            for j in range(len(layer)):
                error = 0.0
                for node in network[i+1]:
                    error += (node['weights'][j] * node['delta'])
                errors.append(error)
        else: #output layer
            for j in range(len(layer)):
                node = layer[j]
                errors.append(expected[j] - node['output'])
        for j in range(len(layer)):
            node = layer[j]
            node['delta'] = errors[j] * transfer_derivative(node['output'])
    
def update_weights(network, row, eta):
    for i in range(len(network)):
        inputs = row[:-1]
        if i != 0:
            inputs = [node['output'] for node in network[i-1]]
        for node in network[i]:
            for j in range(len(inputs)):
                node['weights'][j] += eta * node['delta'] * inputs[j]
            node['weights'][-1] += eta * node['delta']

def train_network(network, train, eta, num_epochs, num_outputs):
    for epoch in range(num_epochs):
        sum_error = 0
        for row in train:
            outputs = forward_propagate(network, row)
            expected = [0 for i in range(n_outputs)]
            expected[row[-1]] = 1
            sum_error += sum([(expected[i] - outputs[i])**2 for i in range(len(expected))])
            backward_propagate_error(network, expected)
            update_weights(network, row, eta)
        print('>epoch=%d, lrate=%.3f, error=%.3f' % (epoch, eta, sum_error))

if __name__ == "__main__":
    dataset1 = [[2.7810836,2.550537003,0],
        [1.465489372, 2.362125076, 0],
        [3.396561688, 4.400293529, 0],
        [1.38807019, 1.850220317, 0],
        [3.06407232,3.005305973,0],
        [7.627531214,2.759262235,1],
        [5.332441248,2.088626775,1],
        [6.922596716,1.77106367,1],
        [8.675418651,-0.242068655,1],
        [7.673756466,3.508563011,1]]
    dataset = [[2.7810836,2.550537003,-1],
        [1.465489372, 2.362125076, -1],
        [3.396561688, 4.400293529, -1],
        [1.38807019, 1.850220317, -1],
        [3.06407232,3.005305973,-1],
        [7.627531214,2.759262235,1],
        [5.332441248,2.088626775,1],
        [6.922596716,1.77106367,1],
        [8.675418651,-0.242068655,1],
        [7.673756466,3.508563011,1]]
    n_inputs = len(dataset[0]) - 1
    n_outputs = len(set([row[-1] for row in dataset]))
    network = initialize_network(n_inputs, 2, n_outputs)
    train_network(network, dataset, 0.5, 20, n_outputs)
    for layer in network:
        print('layer \n', layer)