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
            hitbox = self.car.hitbox(batch, background)
            return car, intersectEyes, eyes, hitbox
        return car, intersectEyes

    def generateHitbox(self):
        hitbox = self.car.generateHitbox()
        return hitbox

    def move(self, dt):
        if self.step < self.maxStep:
            inputnn = self.car.observation
            instruction = self.nn.feedforward(inputnn)
            self.step += 1
            
            self.car.updateGA(dt, instruction)
        else:
            self.dead = True

    def update(self, dt):
        if not self.dead:
            self.move(dt)

            pos = self.car.position
            if(pos.x < 2 or pos.y < 2 or pos.x > self.window.x-2 or pos.y > self.window.y-2):
                self.dead = True
        else:
            self.car.dead = self.dead

    def calcFitness(self):
        self.fitness = (self.car.currentCheckpoint*1000)/(self.step**2) 

    def clone(self, carX, carY, best=False):
        baby = Agent(carX, carY, window=self.window, best=best)
        baby.nn = self.nn.clone()
        return baby