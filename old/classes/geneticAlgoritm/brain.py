import random

class Brain:
    def __init__(self, count) -> None:
        self.instructions = [random.randint(0, 3) for _ in range(count)]
        self.step = 0

    def clone(self):
        clone = Brain(len(self.instructions))
        clone.instructions = self.instructions[:]
        return clone

    def mutate(self):
        mutationRate = 0.01
        for i in range(len(self.instructions)):
            rand = random.random()
            if(rand < mutationRate):
                self.instructions[i] = random.randint(0, 3)