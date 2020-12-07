from classes.car import Car
from classes.geneticAlgoritm.brain import Brain

class Agent:
    def __init__(self, window, goal, best=False):
        self.car = Car(300, 200)
        self.window = window
        self.dead = self.car.dead
        self.finished = self.car.finished
        self.fitness = 0
        
        self.brain = Brain(5000)
        self.goal = goal
        self.bestCar = best
        
    def draw(self, batch, group):
        car = self.car.draw(batch, group, self.bestCar)
        return car

    def move(self, dt):
        if(self.brain.step < len(self.brain.instructions)):
            instruction = self.brain.instructions[self.brain.step]
            self.brain.step += 1
            
            self.car.updateGA(dt, instruction)
        else:
            self.car.dead = True
            self.dead = True

    def update(self, dt):
        if not self.car.dead and not self.car.finished:
            self.move(dt)

            pos = self.car.position
            if(pos.x < 2 or pos.y < 2 or pos.x > self.window.x-2 or pos.y > self.window.y-2):
                self.car.dead = True
                self.dead = True
            elif(abs(self.goal - pos) < 10):
                self.car.finished = True
                self.finished = True

    def calcFitness(self):
        if self.car.finished or self.finished:
            self.fitness = 1/16 + 10000/(self.brain.step**2)
        else:
            self.fitness = 1/(abs(self.goal - self.car.position)**2)

    def clone(self, best=False):
        baby = Agent(window=self.window,goal=self.goal, best=best)
        baby.brain = self.brain.clone()
        return baby