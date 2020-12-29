import numpy as np
import random

class NeuralNetwork:
    def __init__(self):
        self.inputSize = 6
        self.outputSize = 4
        self.hiddenSize = 16  
        self.W1 = np.random.randn(self.inputSize, self.hiddenSize)
        self.W2 = np.random.randn(self.hiddenSize, self.outputSize)

        self.weights = np.array(np.random.randn(self.inputSize, self.hiddenSize), np.random.randn(self.hiddenSize, self.outputSize), dtype=np.float32)

    def relu(self, x):
        return np.maximum(0, x)        

    def feedforward(self, X):
        inputEyes = [100000 if v is None else v for v in X]
        
        self.dot1 = np.dot(inputEyes, self.weights[0])
        self.activation1 = self.relu(self.dot1)
        self.dot2 = np.dot(self.activation1, self.weights[1])
        self.activation2 = self.relu(self.dot2)

        max_output = max(self.activation2)
        index = np.where(self.activation2 == max_output)
        instruction = index[0][0]
        return instruction

    def saveWeights(self):
        np.savetxt("w1.txt", self.weights[0], fmt="%s")
        np.savetxt("w2.txt", self.weights[1], fmt="%s")

    def clone(self):
        clone = NeuralNetwork()
        clone.W1 = self.W1
        clone.W2 = self.W2
        clone.weights = self.weights
        return clone

    def mutate(self):
        mutationRate = 0.01
        for weight in self.weights:
            for i in range(weight.shape[0]):
                for j in range(weight.shape[1]):
                    rand = random.random()
                    if(rand < mutationRate):
                        weight[i,j] += random.uniform(-1, 1)

if __name__ == "__main__":
    nn = NeuralNetwork()

    # print("NN1:")
    # print(nn.W1)
    # print(" ")
    # print(nn.W2)
    # print(" ")

    nn2 = NeuralNetwork()

    # print(" ")
    # print("NN2 1:")
    # print(nn2.W1)
    # print(" ")
    # print(nn2.W2)
    # print(" ")

    nn2.W1 = nn.W1
    nn2.W2 = nn.W2
    
    # print(" ")
    # print("NN2 2:")
    # print(nn2.W1)
    # print(" ")
    # print(nn2.W2)
    # print(" ")

    nn_input = [5, 3, 5, 1, 7, 8]

    output = nn.feedforward(nn_input)
    output2 = nn2.feedforward(nn_input)

    if output == output2:
        print("True")
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

    if output2 == 0:
        print(0)
    elif output2 == 1:
        print(1)
    elif output2 == 2:
        print(2)
    elif output2 == 3:
        print(3)
    else:
        print("Number is not an int of 0-3")
        print(output)

    # print(nn.W1)
    # print(" ")
    # print(nn.W2)
    # print(" ")

    # test = 100
    # while test < 100:
    #     nn.mutate()
    #     test += 1
    
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