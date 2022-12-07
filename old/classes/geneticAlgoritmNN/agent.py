from classes.car import Car
from classes.geneticAlgoritmNN.neuralNetwork import NeuralNetwork
from classes.improvedLine import linline
from classes.Vector import Vector2D

from math import inf

class Agent:
    def __init__(self, carX, carY, window, best=False, scale: float = 1.48):
        self.car = Car(carX, carY, scale)
        self.scale = scale
        self.window = window
        self.dead = self.car.dead
        self.fitness = 0
        self.step = 0
        self.maxStep = 500
        self.reset = False
        self.reset2 = False
        
        self.nn = NeuralNetwork()
        self.bestCar = best

        self.index = 0
        
    def draw(self, batch, foreground, background, vertices, show):
        car = self.car.draw(batch, foreground, self.bestCar)
        # intersectEyes = self.car.intersectEyes(batch, vertices, background)
        # if show or not self.dead:
            # eyes = self.car.eyes(batch, background)
            # hitbox = self.car.hitbox(batch, background)
            # return car, intersectEyes, eyes, hitbox
            # return car, intersectEyes, eyes
        # return car, intersectEyes
        return car

    def generateHitbox(self):
        hitbox = self.car.generateHitbox()
        return hitbox

    def move(self, dt, vertices):
        if self.step < self.maxStep:
            inputnn = []
            self.car.mathIntersect(vertices)
            inputnn = self.car.observe()
            if len(inputnn) > 7:
                instruction = self.nn.feedforward(inputnn)
            else:
                instruction = 3
                print(f"Input: {inputnn}")
            self.step += 1
            
            self.car.updateWithInstruction(dt, instruction)
        else:
            self.dead = True

    def update(self, dt, vertices):
        if not self.dead:
            if self.car.currentCheckpoint > 1 and self.reset == False:
                self.maxStep += 1000
                self.reset = True
            if self.car.currentCheckpoint > 2 and self.reset2 == False:
                self.maxStep += 1000
                self.reset2 = True
            self.move(dt, vertices)

            pos = self.car.position
            if(pos.x < 2 or pos.y < 2 or pos.x > self.window.x-2 or pos.y > self.window.y-2):
                self.dead = True
        else:
            self.car.dead = self.dead

    def calcFitness(self, skeletonLines, checkpoints, blindSpot, blindIndex):        
        if self.car.currentCheckpoint > 0 or self.car.currentLap > 0:
            if self.car.currentCheckpoint >= checkpoints:
                self.car.currentLap += 1
                self.car.currentCheckpoint = 0
            minimum = 100000
            minLine = None
            for line in skeletonLines:
                distance = d if (d:=line.distance(self.car.position)) != None else 99999 
                if distance < minimum:
                    minimum = distance
                    minLine = line
            if minimum > 80:
                minDistance = 100000
                minSpot = None
                for spot in blindSpot:
                    distance = abs(self.car.position - spot)
                    if distance < minDistance:
                        minDistance = distance
                        minSpot = spot
                indexSpot = blindSpot.index(minSpot)
                index = blindIndex[indexSpot]
                minLine = skeletonLines[index]
            else:
                index = skeletonLines.index(minLine)

            linesToIndex = skeletonLines[:index]
            distanceToIndex = 0
            for line in linesToIndex:
                startPointLine, endPointLine = line.getEndPoints()
                distanceToIndex += abs(endPointLine - startPointLine)

            lineToOutside = linline.fromVector(minLine.n, self.car.position) #BC
            intersection = lineToOutside.intersect(minLine) #B
            startPoint, _ = minLine.getEndPoints() #A
            if startPoint.x == None:
                distanceLine = 0
            elif startPoint.y == None: 
                distanceLine = 0
            elif intersection == None:
                distanceLine = 0
            else:
                distanceLine = intersection - startPoint #AB

            if index > 10 and self.car.currentCheckpoint < 3:
                self.fitness = 0
            else:
                self.fitness = ((self.car.currentLap * 100) + (abs(distanceLine)*100)+distanceToIndex*100)**2/self.step
            self.index = index
        else:
            self.fitness = 0

    def clone(self, carX, carY, best):
        baby = Agent(carX, carY, window=self.window, best=best, scale=self.scale)
        baby.nn = self.nn.clone()
        return baby