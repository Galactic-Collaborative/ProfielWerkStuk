import numpy as np
import math

class NeuralNetwork():
    def __init__(self, inputEyes):
        self.input      = inputEyes
        self.weights1   = np.random.rand(self.input.shape[1],4) 
        self.weights2   = np.random.rand(4,1)      

    def relu(self, x):
        return np.maximum(0,x)          

    def feedforward(self):
        self.layer1 = self.relu(np.dot(self.input, self.weights1))
        self.output = self.relu(np.dot(self.layer1, self.weights2))