import pyglet
from classes.Vector import Vector2D
from classes.car import Car
import random 
import math

running = True

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

class Agent:
    def __init__(self, window, goal, best=False):
        self.car = Car(10, 10)
        self.window = window
        self.dead = self.car.dead
        self.finished = self.car.finished
        self.fitness = 0
        
        self.brain = Brain(10000)
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

class World:
    def __init__(self, cars, window) -> None:
        self.window = Vector2D.fromTuple(window)
        self.goal = self.window
        self.carList = [Agent(window=self.window, goal=(self.goal-Vector2D(10,10))) for _ in range(cars)]

        self.fitnessSum = 0
        self.gen = 1

        self.bestCar = 0

        self.minStep = 1000

    def draw(self, batch, group):
        drawList = [car.draw(batch, group) for car in self.carList]
        return drawList

    def update(self, dt):
        for car in self.carList:
            if car.brain.step > self.minStep:
                car.dead = True
            else:
                car.update(dt)

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

        nextGen.append(self.carList[self.bestCar].clone(best=True))
        for _ in range(1, len(self.carList)):
            parent = self.selectParent()
            if parent != None:
                nextGen.append(parent.clone())

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

### MAIN LOOP
window = pyglet.window.Window(resizable=True, fullscreen=True)

world = World(100, window=window.get_size())
batch = pyglet.graphics.Batch()
running = True

@window.event
def on_close():
    running = False

@window.event
def on_draw():
    render()

def update(dt):
    if(world.allCarsDead()):
        world.calcFitness()
        world.naturalSelection()
        world.mutateAll()
    else:
        world.update(dt)

def render():
    window.clear()
    foreground = pyglet.graphics.OrderedGroup(0)
    carDrawings = world.draw(batch, foreground)
    goal = pyglet.shapes.Circle(window.get_size()[0]-10, window.get_size()[1]-10, 10, color=(0,255,0), batch=batch)
    batch.draw()

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1/120.0)
    pyglet.app.run()