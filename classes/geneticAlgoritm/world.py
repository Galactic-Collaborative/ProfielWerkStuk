import random
from classes.Vector import Vector2D
from classes.geneticAlgoritm.agent import Agent

class World:
    def __init__(self, cars, carX, carY, window) -> None:
        self.window = Vector2D.fromTuple(window)
        self.goal = self.window
        self.carX = carX
        self.carY = carY
        self.carList = [Agent(carX, carY, window=self.window, goal=(self.goal-Vector2D(10,10))) for _ in range(cars)]

        self.fitnessSum = 0
        self.gen = 1

        self.bestCar = 0

        self.minStep = 1000

    def draw(self, batch, foreground, background, vertices):
        drawList = [car.draw(batch, foreground, background, vertices) for car in self.carList]
        return drawList

    def update(self, dt):
        for car in self.carList:
            if car.brain.step > self.minStep:
                car.dead = True
            else:
                car.update(dt)

    def generateHitbox(self, car):
        hitbox = car.generateHitbox()
        return hitbox
        
    def allCarsDead(self) -> bool:
        for car in self.carList:
            if not car.dead and not car.finished:
                return False
        return True

    def calcFitness(self):
        for car in self.carList:
            car.calcFitness()

    def naturalSelection(self):
        nextGen = []
        self.setBestCar()
        self.calcFitnessSum()

        nextGen.append(self.carList[self.bestCar].clone(self.carX, self.carY, best=True))
        for _ in range(1, len(self.carList)):
            parent = self.selectParent()
            if parent != None:
                nextGen.append(parent.clone(self.carX, self.carY))

        self.carList = nextGen[:]
        self.gen += 1
        print(f"NEXT GEN: {self.gen}")

    def mutateAll(self):
        for i in range(1, len(self.carList)):
            self.carList[i].brain.mutate()

    def selectParent(self):
        rand = random.random() * self.fitnessSum
        runningSum = 0

        for car in self.carList:
            runningSum += car.fitness
            if runningSum > rand:
                return car

        return None

    def calcFitnessSum(self):
        fitnessSum = 0
        for car in self.carList:
            fitnessSum += car.fitness
        self.fitnessSum = fitnessSum

    def setBestCar(self):
        topFitness = 0
        self.bestCar = 0
        for i, car in enumerate(self.carList):
            if(car.fitness > topFitness):
                topFitness = car.fitness 
                self.bestCar = i

        if(self.carList[self.bestCar].finished):
            self.minStep = self.carList[self.bestCar].brain.step