import numpy as np 

def read_data():
    logical_and = np.array([[0,0,-1],[0,1,-1],[1,0,-1],[1,1,1]])
    logical_or = np.array([[0,0,-1],[0,1,1],[1,0,1],[1,1,1]])
    xor = np.array([[0,0,1,1],[0,1,0,1],[0,1,1,0]])
    data = logical_and
    X = data[:, :-1] #features
    y = data[:,-1] #class 
    return X, y

def compute_perceptron_output(features, weights, bias):
    sum = 0
    for i in range(len(features)):
        sum += weights[i] * features[i]
    sum += bias
    return np.sign(sum)

def perceptron(X, y):
    max_iterations = 10
    num_features = len(X[0])
    weights = [1.0] * num_features
    bias = 0.0
    total = len(X)
    for index in range(max_iterations):
        print('Epoch', index+1, ":")
        right = 0
        for i in range(len(X)):
            instance = X[i]
            label = y[i]
            #prediction = a
            prediction = compute_perceptron_output(instance, weights, bias)
            print(' prediction of ', instance, ' is ', prediction)
            if label * prediction <= 0: #wrong adjust weight and bias
                bias += label
                for feature_num in range(len(instance)):
                    weights[feature_num] += label * instance[feature_num]
                    print('     wrong, adjust weights to', weights, 'bias', bias)
            else: #right
                right += 1
                print('     Correct!')
            if index == 0:
                print('     weights', weights, 'bias', bias)
        if right == total:
            print('Convergence!')
            break
        print(' epoch', index+1, 'average accuracy', float(right)/float(total),'weights',weights,'bias',bias)

if __name__ == "__main__":
    X, y = read_data()
    perceptron(X, y)