from __future__ import annotations

import numpy as np
import random

class NeuralNetwork:
    def __init__(self):
        self.inputSize = 8
        self.outputSize = 4
        self.hiddenSize = 16  
        self.W1 = np.random.randn(self.inputSize, self.hiddenSize)
        self.W2 = np.random.randn(self.hiddenSize, self.outputSize) 
        self.mutationRate = 0.25

    def relu(self, x):
        return np.maximum(0, x)        

    def feedforward(self, inputnn):
        inputEyes = [100000 if v is None else v for v in inputnn]
        
        self.dot1 = np.dot(inputEyes, self.W1)
        self.activation1 = self.relu(self.dot1)
        self.dot2 = np.dot(self.activation1, self.W2)
        self.activation2 = self.relu(self.dot2)

        max_output = max(self.activation2)
        index = np.where(self.activation2 == max_output)
        instruction = index[0][0]
        return instruction

    def saveWeights(self):
        print(self.W1)
        print(self.W2)
        np.savetxt("w1.txt", self.W1, fmt="%s")
        np.savetxt("w2.txt", self.W2, fmt="%s")

        np.save("binaryW1SIGMA", self.W1)
        np.save("binaryW2SIGMA", self.W2)

    def autoSaveWeights(self):
        np.savetxt("autoSave1.txt", self.W1, fmt="%s")
        np.savetxt("autoSave2.txt", self.W2, fmt="%s")

        np.save("binaryW1SIGMA", self.W1)
        np.save("binaryW2SIGMA", self.W2)

    def loadWeights(self):
        self.W1 = np.load("binaryW1SIGMA.npy")
        self.W2 = np.load("binaryW2SIGMA.npy")

    def clone(self):
        clone = NeuralNetwork()
        clone.W1 = np.copy(self.W1)
        clone.W2 = np.copy(self.W2)
        clone.mutationRate = self.mutationRate
        return clone

    def mutate(self):
        self.mutateFunction(self.W1)
        self.mutateFunction(self.W2)

    def mutateFunction(self, weight):
        for i in range(len(weight)):
            rand = random.random()
            if(rand < self.mutationRate):
                weight[i] += random.uniform(-1, 1)

    def crossParent(self, car: NeuralNetwork):
        parent = NeuralNetwork()
        parent.W1 = np.copy(self.W1)
        parent.W2 = np.copy(car.W2)
        parent.mutationRate = 0.5 * (self.mutationRate + car.mutationRate)
        return parent

if __name__ == "__main__":
    nn = NeuralNetwork()

    print("NN1:")
    print(nn.W1)
    print(" ")
    print(nn.W2)
    print(" ")

    nn2 = NeuralNetwork()

    print(" ")
    print("NN2 1:")
    print(nn2.W1)
    print(" ")
    print(nn2.W2)
    print(" ")

    nn2.W1 = nn.W1
    nn2.W2 = nn.W2
    
    # print(" ")
    # print("NN2 2:")
    # print(nn2.W1)
    # print(" ")
    # print(nn2.W2)
    # print(" ")

    nn3 = nn.clone()

    # print(" ")
    # print("NN3:")
    # print(nn3.W1)
    # print(" ")
    # print(nn3.W2)
    # print(" ")

    nn_input = [5, 3, 5, 1, 7, 8, 4, 8]

    output = nn.feedforward(nn_input)
    output2 = nn2.feedforward(nn_input)

    if output == output2:
        print("True")
    if output == 0 or output == 1 or output == 2 or output == 3:
        print(output)
    else:
        print("Number is not an int of 0-3")
        print(output)

    if output2 == 0 or output2 == 1 or output2 == 2 or output2 == 3:
        print(output2)
    else:
        print("Number is not an int of 0-3")
        print(output2)

    random = random.uniform(-1, 1)

    print(random)
    # print(nn.W1)
    # print(" ")
    # print(nn.W2)
    # print(" ")

    # test = 100
    # while test < 100:
    #     nn.mutate()
    #     test -= 1
    
    # output = nn.feedforward(nn_input)

    # if output == 0:
    #     print(0)
    # elif output == 1:
    #     print(1)
    # elif output == 2:
    #     print(2)
    # elif output == 3:
    #     print(3)
    # else:
    #     print("Number is not an int of 0-3")
    #     print(output)

    # print(nn.W1)
    # print(" ")
    # print(nn.W2)