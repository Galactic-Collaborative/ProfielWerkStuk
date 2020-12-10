import pyglet
import math
from classes.improvedLine import linline
from classes.Vector import Vector2D

class Car():
    def __init__(self, x: int, y: int):
        self.mass = 1
        self.forces = Vector2D(0,0)
        self.acceleration = Vector2D(0,0)
        self.velocity = Vector2D(0,0)
        self.position = Vector2D(x, y)

        self.sprites = {"alive": pyglet.resource.image('img/car.png'),"best": pyglet.resource.image('img/carBest.png'),"dead": pyglet.resource.image('img/carCrash.png')}
        self.image_dimensions = (self.sprites['alive'].width, self.sprites['alive'].height)
        self.scale = 1.48

        self.carRotation = Vector2D(1,1)

        self.eyesList = [[0, 500], [500, 500], [500, 0], [500, -500], [0, -500], [-500, 0]]
        self.hitboxVectors = [[3, 3], [33, 3], [33, 23], [3, 23]]
        self.dead = False
        self.middle = Vector2D(0,0)
        
        self.lines = []
        
        self.observation = [None] * len(self.eyesList)

        #GA
        self.bestCar = False
        self.fitness = 0

    def draw(self, batch, group, best=False):
        car = self.drawCar(batch, group, best)
        return car

    def drawCar(self, batch, group, best):
        if self.dead:
            car = pyglet.sprite.Sprite(self.sprites['dead'], x=self.position.x, y=self.position.y, batch=batch, group=group)
        elif best:
            car = pyglet.sprite.Sprite(self.sprites['best'], x=self.position.x, y=self.position.y, batch=batch, group=group)    
        else:
            car = pyglet.sprite.Sprite(self.sprites['alive'], x=self.position.x, y=self.position.y, batch=batch, group=group)

        car.scale = self.scale
        car.anchor_x = car.width // 2
        car.anchor_y = car.height // 2
        car.rotation = -(self.carRotation.rotation())
        return car

    def eyes(self, batch, group):
        eyes = self.drawEyes(batch, group)
        return eyes

    def drawEyes(self, batch, group):
        lines = self.generateLines()
        out = []

        for line in lines:
            out.append(line.draw(batch, group, [1920, 1080], 5))
        return out

    def generateLines(self):
        lines = []
        eyePoints = [Vector2D(i[0],i[1]) for i in self.eyesList]

        for line in eyePoints:
            secondPosition = self.middle + line.rotate(self.carRotation.rotation())
            lines.append(linline.fromPoints(self.middle, secondPosition))

        self.lines = lines
        return lines

    def hitbox(self, batch, group):
        hitboxVectors = self.generateHitbox()
        out = []

        for hitboxLine in hitboxVectors:
            out.append(hitboxLine.draw(batch, group))
        return out

    def generateHitbox(self):
        hitbox = []
        hitboxVectors = [Vector2D(i[0],i[1]) for i in self.hitboxVectors]
        previousPoint = self.position + Vector2D(5, 5)
        lineColor = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]

        for i in range(len(hitboxVectors)):
            j = (i+1)%len(hitboxVectors)
            nextPoint = self.position + hitboxVectors[j].rotate(self.carRotation.rotation())
            l = linline.fromPoints(previousPoint, nextPoint)
            l.color = lineColor[i]
            hitbox.append(l)
            previousPoint = nextPoint
        
        return hitbox

    def intersectEyes(self, batch, lines, group):
        dots = []

        for n, eyeline in enumerate(self.lines):
            intersect = [l.intersect(eyeline) for l in lines if l.intersect(eyeline) != None]
            minList = [abs(self.middle - point) for point in intersect]
            self.observation[n] = 1000
            if len(minList):
                pointIndex = [i for i, j in enumerate(minList) if j == min(minList)]
                point = intersect[pointIndex[0]]
                self.observation[n] = abs(self.middle - point)
                dots.append(pyglet.shapes.Circle(point.x, point.y, 5, color=(255,0,0), batch=batch, group=group))
        return dots

    def forward(self):
        self.forces += Vector2D(100,0)

    def backward(self):
        self.forces += Vector2D(-100,0)

    def left(self):
        self.forces += Vector2D(0, self._getTurnForce())

    def right(self):
        self.forces += Vector2D(0,-self._getTurnForce())

    def update(self, dt, key, key_handler):
        self.forces = Vector2D(0,0)

        if key_handler[key.UP]:
            self.forward()
        if key_handler[key.DOWN]:
            self.backward()
        if key_handler[key.LEFT]:
            self.left()
        if key_handler[key.RIGHT]:
            self.right()
        
        self._calculatePhysics(dt)

    def updateGA(self, dt, instruction):
        self.forces = Vector2D(0,0)

        if(instruction == 0):
            self.forward()
        elif(instruction == 1):
            self.backward()
        elif(instruction == 2):
            self.left()
        elif(instruction == 3):
            self.right()
        else:
            print("Random is not done well")
        
        self._calculatePhysics(dt)

    def _getTurnForce(self):
        if self.velocity.x != 0:
            c = 10
            sigmoid = lambda x : 1 / (1 + math.e**-(x-c))

            sidewayForce = 1/sigmoid(abs(self.velocity)) * 40
        else:
            sidewayForce = 0
        #return sidewayForce
        return 400

    def _calculatePhysics(self, dt):
        #Calculate acceleration based on forces andl limit it to 100 pixels per second per second
        self.acceleration = self.forces.rotate(self.carRotation.rotation()) / self.mass
        self.acceleration.limit(100)

        #Calculate velocity based on accelation and limit it to 200 pixels per second
        self.velocity += self.acceleration * dt
        self.velocity.limit(200)
        
        #Determine if we are driving backwards or forwards
        backwards = (self.velocity @ self.carRotation < 0)

        self.position += self.velocity * dt
        if not backwards:
            self.carRotation = self.velocity.copy()
        else:
            self.carRotation = -self.velocity.copy()
        
        self.middle = self.position + Vector2D.fromTuple(self.image_dimensions).rotate(self.carRotation.rotation()) * self.scale * 0.5
        


"""
        if self.velocity.x != 0:
            self.carRotation = self.velocity.copy()
            self.carRotation.normalize()

        if self.reverse == True:
            if (self.velocity.x < 0 and velocityPrevious.x >= 0) or (self.velocity.x >= 0 and velocityPrevious.x < 0):
                self.reverse2 = True
        else:
            if (self.velocity.x < 0 and velocityPrevious.x >= 0) or (self.velocity.x >= 0 and velocityPrevious.x < 0):
                self.reverse2 = False

        if self.reverse2 == False:
            self.position += self.carRotation * abs(self.velocity) * dt
            self.carRotation.rotation() = self.carRotation.rotation()
        else:
            self.carRotation.rotate(180)
            self.velocity.limit(100)
            self.position += self.carRotation * -abs(self.velocity) * dt
            self.carRotation.rotation() = self.carRotation.rotation()
        self.middle = self.position + Vector2D(25, 15).rotate(self.carRotation.rotation())"""
