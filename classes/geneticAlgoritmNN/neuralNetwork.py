import numpy as np
import random

class NeuralNetwork:
    def __init__(self):
        self.inputSize = 6
        self.outputSize = 4
        self.hiddenSize = 16  
        self.W1 = np.random.randn(self.inputSize, self.hiddenSize)
        self.W2 = np.random.randn(self.hiddenSize, self.outputSize) 

    def relu(self, x):
        return np.maximum(0, x)        

    def feedforward(self, X):
        inputEyes = [100000 if v is None else v for v in X]
        
        self.dot1 = np.dot(inputEyes, self.W1)
        self.activation1 = self.relu(self.dot1)
        self.dot2 = np.dot(self.activation1, self.W2)
        self.activation2 = self.relu(self.dot2)

        max_output = max(self.activation2)
        index = np.where(self.activation2 == max_output)
        instruction = index[0][0]
        return instruction

    def saveWeights(self):
        np.savetxt("w1.txt", self.W1, fmt="%s")
        np.savetxt("w2.txt", self.W2, fmt="%s")

    def clone(self):
        clone = NeuralNetwork()
        clone.W1 = self.W1
        clone.W2 = self.W2
        return clone

    def mutate(self):
        mutationRate = 0.01
        for i in range(len(self.W1)):
            for y in range(i):
                for z in range(y):
                    rand = random.random()
                    if(rand < mutationRate):
                        self.W1[i][y][z] = random.uniform(0, 1)
        for i in range(len(self.W2)):
            for y in range(i):
                for z in range(y):
                    rand = random.random()
                    if(rand < mutationRate):
                        self.W2[i][y][z] = random.uniform(0, 1)        

if __name__ == "__main__":
    nn = NeuralNetwork()

    nn_input = [5, 3, 5, 1, 7, 8]

    output = nn.feedforward(nn_input)

    if output == 0:
        print(0)
    elif output == 1:
        print(1)
    elif output == 2:
        print(2)
    elif output == 3:
        print(3)
    else:
        print("Number is not an int of 0-3")
        print(output)

    print(nn.W1)
    print(" ")
    print(nn.W2)
    print(" ")

    test = 100
    while test < 100:
        nn.mutate()
        test += 1
    
    output = nn.feedforward(nn_input)

    if output == 0:
        print(0)
    elif output == 1:
        print(1)
    elif output == 2:
        print(2)
    elif output == 3:
        print(3)
    else:
        print("Number is not an int of 0-3")
        print(output)

    print(nn.W1)
    print(" ")
    print(nn.W2)