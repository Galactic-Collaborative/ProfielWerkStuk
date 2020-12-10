from classes.car import Car
from classes.geneticAlgoritm.brain import Brain

class Agent:
    def __init__(self, carX, carY, window, goal, best=False):
        self.car = Car(carX, carY)
        self.window = window
        self.dead = self.car.dead
        self.finished = self.car.finished
        self.fitness = 0
        
        self.brain = Brain(5000)
        self.goal = goal
        self.bestCar = best
        
    def draw(self, batch, foreground, background, vertices, show):
        car = self.car.draw(batch, foreground, self.bestCar)
        if show:
            eyes = self.car.eyes(batch, background)
            hitbox = self.car.hitbox(batch, background)
            intersectEyes = self.car.intersectEyes(batch, vertices, background)
            return car, eyes, hitbox, intersectEyes
        return car

    def generateHitbox(self):
        hitbox = self.car.generateHitbox()
        return hitbox

    def move(self, dt):
        if(self.brain.step < len(self.brain.instructions)):
            instruction = self.brain.instructions[self.brain.step]
            self.brain.step += 1
            
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
            self.car.finished = self.finished

    def calcFitness(self):
        if self.finished:
            self.fitness = 1/16 + 10000/(self.brain.step**2)
        else:
            self.fitness = 1/(abs(self.goal - self.car.position)**2)

    def clone(self, carX, carY, best=False):
        baby = Agent(carX, carY, window=self.window, goal=self.goal, best=best)
        baby.brain = self.brain.clone()
        return baby