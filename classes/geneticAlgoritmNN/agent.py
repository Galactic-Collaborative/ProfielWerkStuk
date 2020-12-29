from classes.car import Car
from classes.geneticAlgoritmNN.neuralNetwork import NeuralNetwork

class Agent:
    def __init__(self, carX, carY, window, best=False):
        self.car = Car(carX, carY)
        self.window = window
        self.dead = self.car.dead
        self.fitness = 0
        self.step = 0
        self.maxStep = 1000
        
        self.nn = NeuralNetwork()
        self.bestCar = best
        
    def draw(self, batch, foreground, background, vertices, show):
        car = self.car.draw(batch, foreground, self.bestCar)
        intersectEyes = self.car.intersectEyes(batch, vertices, background)
        if show or not self.dead:
            eyes = self.car.eyes(batch, background)
            # hitbox = self.car.hitbox(batch, background)
            # return car, intersectEyes, eyes, hitbox
            return car, intersectEyes, eyes
        return car, intersectEyes

    def generateHitbox(self):
        hitbox = self.car.generateHitbox()
        return hitbox

    def move(self, dt, vertices):
        if self.step < self.maxStep:
            inputnn = []
            self.car.mathIntersect(vertices)
            for point in self.car.circuitIntersections:
                inputnn.append(abs(self.car.middle - point)) 
            if len(inputnn) > 5:
                instruction = self.nn.feedforward(inputnn)
            else:
                instruction = 3
                # print(f"Input: {inputnn}")
            self.step += 1
            
            self.car.updateWithInstruction(dt, instruction)
        else:
            self.dead = True

    def update(self, dt, vertices):
        if not self.dead:
            self.move(dt, vertices)

            pos = self.car.position
            if(pos.x < 2 or pos.y < 2 or pos.x > self.window.x-2 or pos.y > self.window.y-2):
                self.dead = True
        else:
            self.car.dead = self.dead

    def calcFitness(self, outsideLines):
        minimum = 100000
        for line in outsideLines:
            distance = line.distance(self.car.position)
            if distance < minimum:
                minimum = distance
                minLine = line
        
        index = outsideLines.index(minLine)
        if self.car.currentCheckpoint != 0:
            self.fitness = (self.car.currentCheckpoint*100) + (index*100)/(self.step**2)
        else:
            self.fitness = 0

    def clone(self, carX, carY, best):
        baby = Agent(carX, carY, window=self.window, best=best)
        baby.nn = self.nn.clone()
        return baby