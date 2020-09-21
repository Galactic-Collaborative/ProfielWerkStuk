import pyglet
from classes.Vector import Vector2D
import random
import math


running = True

class Brain:
    def __init__(self, count) -> None:
        self.instructions = [Vector2D.fromAngle(random.random()*2*math.pi) for _ in range(count)]
        self.step = 0
    
    def clone(self):
        clone = Brain(len(self.instructions))
        clone.instructions = self.instructions[:]
        return clone
    
    def mutate(self):
        mutationRate = 0.01 #Chance that vector gets changed
        for i in range(len(self.instructions)):
            rand = random.random()
            if(rand < mutationRate):
                self.instructions[i] = Vector2D.fromAngle(random.random()*2*math.pi) #Set direction to random angle

class Dot:
    def __init__(self, window, goal, best=False) -> None:
        self.pos = Vector2D(100,100)
        self.vel = Vector2D(0,0)
        self.acc = Vector2D(0,0)

        self.goal = goal
        
        self.brain = Brain(1000)
        self.fitness = 0
        self.window = window

        self.bestDot = best
        self.dead = False
        self.finished = False
    
    def draw(self, batch):
        if(self.dead): 
            color = (255,0,0)
            opacity = 100
        elif(self.bestDot):
            color = (0,255,0)
            opacity = 255
        else: 
            color = (255,255,255)
            opacity = 100
        dot = pyglet.shapes.Circle(self.pos.x, self.pos.y, 5, color=color, batch=batch)
        dot.opacity = opacity
        return dot
            
    def move(self):
        if(self.brain.step < len(self.brain.instructions)):
            self.acc = self.brain.instructions[self.brain.step]
            self.brain.step += 1
        else:
            self.dead = True
        
        self.vel += self.acc
        self.vel.limit(5)
        self.pos += self.vel

    def update(self):
        if not self.dead and not self.finished:
            self.move()

            pos = self.pos
            if(pos.x < 2 or pos.y < 2 or pos.x > self.window.x-2 or pos.y > self.window.y-2):
                self.dead = True
            elif(abs(self.goal - self.pos) < 10):
                self.finished = True
    
    def calcFitness(self):
        if self.finished:
            self.fitness = 1/16 + 10000/(self.brain.step**2)
        else:
            self.fitness = 1/(abs(self.goal - self.pos)**2)

    def clone(self, best=False):
        baby = Dot(window=self.window,goal=self.goal, best=best)
        baby.brain = self.brain.clone()
        return baby

class World:
    def __init__(self, dots, window) -> None:
        self.window = Vector2D.fromTuple(window)
        self.goal = self.window
        self.dotList = [Dot(window=self.window,goal=(self.goal-Vector2D(10,10))) for _ in range(dots)]

        self.fitnessSum = 0
        self.gen = 1

        self.bestDot = 0

        self.minStep = 1000
    
    def draw(self, batch):
        drawList = [dot.draw(batch) for dot in self.dotList]
        return drawList
    
    def update(self):
        for dot in self.dotList:
            if dot.brain.step > self.minStep: #If dot has taken more steps than best dot
                dot.dead = True
            else:
                dot.update()
    
    def allDotsDead(self) -> bool:
        for dot in self.dotList:
            if(not(dot.dead) and not(dot.finished)): #If dot is dead or has reached finish, we don't have to check for the rest
                return False
        return True
    
    def calcFitness(self):
        for dot in self.dotList:
            dot.calcFitness()
    
    def naturalSelection(self):
        nextGen = []
        self.setBestDot()
        self.calcFitnessSum()

        nextGen.append(self.dotList[self.bestDot].clone(best=True))
        for _ in range(1, len(self.dotList)):
            parent = self.selectParent()
            nextGen.append(parent.clone())
        
        self.dotList = nextGen[:]
        self.gen+=1
        print(f"NEXT GEN: {self.gen}")
    
    def mutateAll(self):
        for i in range(1,len(self.dotList)):
            self.dotList[i].brain.mutate()


    def selectParent(self):
        rand = random.random() * self.fitnessSum
        runningSum = 0

        for dot in self.dotList:
            runningSum += dot.fitness
            if runningSum > rand:
                return dot
        

        return None

    def calcFitnessSum(self):
        fsum = 0
        for dot in self.dotList: 
            fsum += dot.fitness
        self.fitnessSum = fsum

    def setBestDot(self):
        topFitness = 0
        self.bestDot = 0
        for i, dot in enumerate(self.dotList):
            if(dot.fitness > topFitness):
                topFitness = dot.fitness
                self.bestDot = i
        
        if(self.dotList[self.bestDot].finished):
            self.minStep = self.dotList[self.bestDot].brain.step

### MAIN LOOP
# config = pyglet.gl.Config(sample_buffers=1, samples=4)
window = pyglet.window.Window(resizable=True, fullscreen=True) 

world = World(1000, window=window.get_size())
batch = pyglet.graphics.Batch()
running = True

@window.event
def on_close():
    running = False


@window.event
def on_draw():
    render()

def update(dt):
    if(world.allDotsDead()):
        world.calcFitness()
        world.naturalSelection()
        world.mutateAll()
    else:
        world.update()

def render():
    window.clear()
    drawings = world.draw(batch)
    goal = pyglet.shapes.Circle(window.get_size()[0]-10, window.get_size()[1]-10, 10, color=(0,255,0), batch=batch)
    batch.draw()

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1/120.0)
    pyglet.app.run()

#Setup
