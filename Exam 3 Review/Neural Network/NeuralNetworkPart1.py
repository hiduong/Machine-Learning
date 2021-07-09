import numpy as np

# compute the hidden node activation 
# given the input features, weights, and bias
def activation(weights, features, bias):
    wsum = np.dot(weights, features)
    return np.tanh(wsum +  bias)

print('or')
print(activation([1,1],[-1,-1],0.5))
print(activation([1,1],[-1,1],0.5))
print(activation([1,1],[1,-1],0.5))
print(activation([1,1],[1,1],0.5))

print('\nnand')
print(activation([-1,-1],[-1,-1],1.5))
print(activation([-1,-1],[-1,1],1.5))
print(activation([-1,-1],[1,-1],1.5))
print(activation([-1,-1],[1,1],1.5))

print('\nand')
print(activation([1,1],[-1,-1],-1.5))
print(activation([1,1],[-1,1],-1.5))
print(activation([1,1],[1,-1],-1.5))
print(activation([1,1],[1,1],-1.5))

print('\nxor = and(or, nand)')
print(np.dot([1,1],[-1,1])-1.0)
print(np.dot([1,1],[1,1])-1.0)
print(np.dot([1,1],[1,1])-1.0)
print(np.dot([1,1],[1,-1])-1.0)