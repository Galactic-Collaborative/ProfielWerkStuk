import numpy as np

class NeuralNetwork:
    def __init__(self, inputEyes):
        self.input = inputEyes
        self.inputSize = 6
        self.outputSize = 4
        self.hiddenSize = 16  
        self.W1 = np.random.randn(self.inputSize, self.hiddenSize)
        self.W2 = np.random.randn(self.hiddenSize, self.outputSize) 

    def relu(self, x):
        return np.maximum(0,x)          

    def feedforward(self, X):
        self.dot1 = np.dot(X, self.W1)
        self.activation1 = self.relu(self.dot1)
        self.dot2 = np.dot(self.activation1, self.W2)
        self.activation2 = self.relu(self.dot2)
        return self.activation2

    def saveWeights(self):
        np.savetxt("w1.txt", self.W1, fmt="%s")
        np.savetxt("w2.txt", self.W2, fmt="%s")