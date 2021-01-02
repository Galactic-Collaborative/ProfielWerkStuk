import random
from random import sample
from classes.Vector import Vector2D
from classes.geneticAlgoritmNN.agent import Agent

class World:
    def __init__(self, cars, carX, carY, window, load=False) -> None:
        self.window = Vector2D.fromTuple(window)
        self.carX = carX
        self.carY = carY
        self.carList = [Agent(self.carX, self.carY, window=self.window) for _ in range(cars)]
        self.show = False
        self.showA = True
        self.carCount = cars

        self.fitnessSum = 0
        self.gen = 1

        self.bestCar = 0

        self.maxStep = 1000
        self.load = load

    def draw(self, batch, foreground, background, vertices):
        if self.showA:
            drawList = [car.draw(batch, foreground, background, vertices, self.show) for car in self.carList]
        else:
            car = self.carList[self.bestCar]
            drawList = car.draw(batch, foreground, background, vertices, self.show)
        return drawList

    def update(self, dt, vertices):
        for agent in self.carList:
            if agent.step > self.maxStep:
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
        for _ in range(1, len(self.carList)):
            parent = self.selectParent()
            if parent != None:
                nextGen.append(parent.clone(self.carX, self.carY, best=False))
            else:
                nextGen.append(Agent(self.carX,self.carY,window=self.window,best=False))
            
        self.carList.clear()
        self.carList = nextGen[:]
        del nextGen

    def mutateAll(self):
        for i in range(1, len(self.carList)):
            self.carList[i].nn.mutate()

    def crossParenting(self, x):
        if len(self.carList) > 10:
            selectList = []
            selectList = self.carList[1:]
            for i in range(x):
                newCar = Agent(self.carX,self.carY,window=self.window,best=False)
                randomCars = sample(selectList, 2)
                newCar.nn = randomCars[0].nn.crossParent(randomCars[1].nn)
                if randomCars[0] in self.carList and randomCars[1] in self.carList:
                    if randomCars[0] == randomCars[1]:
                        self.carList.remove(randomCars[0])
                    else:
                        self.carList.remove(randomCars[0])
                        self.carList.remove(randomCars[1])
                self.carList.append(newCar)

        while len(self.carList) != self.carCount:
            self.carList.append(Agent(self.carX,self.carY,window=self.window,best=False))

    def selectParent(self):
        rand = random.random() * self.fitnessSum
        runningSum = 0

        for agent in self.carList:
            runningSum += agent.fitness
            if runningSum > rand:
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