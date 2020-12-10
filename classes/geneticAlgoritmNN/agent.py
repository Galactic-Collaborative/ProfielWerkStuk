from classes.car import Car
from classes.geneticAlgoritmNN.neuralNetwork import NeuralNetwork

class Agent:
    def __init__(self, carX, carY, window, goal, best=False):
        self.car = Car(carX, carY)
        self.window = window
        self.dead = self.car.dead
        self.finished = False
        self.fitness = 0
        self.step = 0
        self.maxStep = 1000
        
        self.nn = NeuralNetwork()
        self.goal = goal
        self.bestCar = best
        
    def draw(self, batch, foreground, background, vertices, show):
        car = self.car.draw(batch, foreground, self.bestCar)
        intersectEyes = self.car.intersectEyes(batch, vertices, background)
        if show:
            eyes = self.car.eyes(batch, background)
            hitbox = self.car.hitbox(batch, background)
            return car, eyes, hitbox
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
        if not self.dead and not self.finished:
            self.move(dt)

            pos = self.car.position
            if(pos.x < 2 or pos.y < 2 or pos.x > self.window.x-2 or pos.y > self.window.y-2):
                self.dead = True
            elif(abs(self.goal - pos) < 10):
                self.finished = True
        else:
            self.car.dead = self.dead

    def calcFitness(self):
        if self.finished:
            self.fitness = 1/16 + 10000/(self.brain.step**2)
        else:
            self.fitness = 1/(abs(self.goal - self.car.position)**2)

    def clone(self, carX, carY, best=False):
        baby = Agent(carX, carY, window=self.window, goal=self.goal, best=best)
        baby.nn = self.nn.clone()
        return baby