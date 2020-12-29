import random
from classes.Vector import Vector2D
from classes.geneticAlgoritmNN.agent import Agent

class World:
    def __init__(self, cars, carX, carY, window) -> None:
        self.window = Vector2D.fromTuple(window)
        self.carX = carX
        self.carY = carY
        self.carList = [Agent(self.carX, self.carY, window=self.window) for _ in range(cars)]
        self.show = False
        self.showA = True

        self.fitnessSum = 0
        self.gen = 1

        self.bestCar = 0

        self.minStep = 1000

    def draw(self, batch, foreground, background, vertices):
        if self.showA:
            drawList = [car.draw(batch, foreground, background, vertices, self.show) for car in self.carList]
        else:
            car = self.carList[self.bestCar]
            drawList = car.draw(batch, foreground, background, vertices, self.show)
        return drawList

    def update(self, dt, vertices):
        for agent in self.carList:
            if agent.step > self.minStep:
                agent.dead = True
            else:
                agent.update(dt, vertices)

    def generateHitbox(self, agent):
        hitbox = agent.generateHitbox()
        return hitbox
        
    def allCarsDead(self) -> bool:
        for car in self.carList:
            if not car.dead:
                return False
        return True

    def calcFitness(self, outsideLines):
        for car in self.carList:
            car.calcFitness(outsideLines)

    def naturalSelection(self):
        self.gen += 1
        print("------------------------------------------------------------------------------------------------------------------------------")
        print(f"NEXT GEN: {self.gen}")

        check = []
        check2 = []
        for agent in self.carList:
            check.append(agent.car.currentCheckpoint)
            check2.append(agent.fitness)
        print(" ")
        print("Current Checkpoint:")
        print(check)
        print(" ")
        print("Fitness:")
        print(check2)

        nextGen = []
        self.setBestCar()
        self.calcFitnessSum()

        nextGen.append(self.carList[self.bestCar].clone(self.carX, self.carY, best=True))
        # for _ in range(1, len(self.carList)):
        #     parent = self.selectParent()
        #     if parent == None:
        #         nextGen.append(Agent(self.carX, self.carY, window=self.window, best=False))
        #     else:
        #         nextGen.append(parent.clone(self.carX, self.carY, best=False))

        for _ in range(1, len(self.carList)):
            nextGen.append(self.carList[self.bestCar].clone(self.carX, self.carY, best=False))

        self.carList.clear()
        self.carList = nextGen[:]
        del nextGen

    def mutateAll(self):
        for i in range(1, len(self.carList)):
            print(f"Car: {i}")
            self.carList[i].nn.mutate()

    def selectParent(self):
        rand = random.random() * self.fitnessSum
        runningSum = 0

        for agent in self.carList:
            runningSum += agent.fitness
            if runningSum > rand:
                # print(agent)
                return agent
        return None

    def calcFitnessSum(self):
        fitnessSum = 0
        for car in self.carList:
            fitnessSum += car.fitness
        self.fitnessSum = fitnessSum

    def setBestCar(self):
        topFitness = 0
        
        for i, car in enumerate(self.carList):
            if(car.fitness > topFitness):
                topFitness = car.fitness 
                self.bestCar = i
        print(f"Best Car: {self.bestCar}")