import pyglet
import math
from classes.line import linline
from classes.Vector import Vector2D
from classes.line import linline

class Car():
    def __init__(self, x: int, y: int):
        self.position = Vector2D(x, y)
        self.acceleration = Vector2D(0,0)
        self.velocity = Vector2D(0,0)
        self.mass = 1
        self.rotation = 0
        self.carRotation = Vector2D(0,0)
        self.reverse = False
        self.reverse2 = False
        self.eyesList = [[0, 200], [200, 200], [200, 0], [200, -200], [0, -200], [-200, 0]]
        self.hitboxVectors = [[3, 3], [35, 3], [35, 25], [3, 25]]
        self.dead = False
        self.lines = []
        self.middle = Vector2D(0,0)

    def draw(self, batch, group):
        car = self.drawCar(batch, group)
        return car

    def drawCar(self, batch, group):
        if not self.dead:
            car = pyglet.sprite.Sprite(pyglet.resource.image('img/car.png'), x=self.position.x, y=self.position.y, batch=batch, group=group)
        else:
            car = pyglet.sprite.Sprite(pyglet.resource.image('img/car2.png'), x=self.position.x, y=self.position.y, batch=batch, group=group)
        car.scale = 0.15
        car.anchor_x = car.width // 2
        car.anchor_y = car.height // 2
        car.rotation = -(self.rotation)
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
            secondPosition = self.middle + line.rotate(self.rotation)
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
            nextPoint = self.position + hitboxVectors[j].rotate(self.rotation)
            l = linline.fromPoints(previousPoint, nextPoint)
            l.color = lineColor[i]
            hitbox.append(l)
            previousPoint = nextPoint

        return hitbox

    def intersectEyes(self, batch, lines, group):
        dots = []

        for eyeline in self.lines:
            intersect = []
            for laneline in lines:
                intersect.append(laneline.intersect(eyeline))

            minList = [abs(self.middle - point) for point in intersect if point != None]
            if len(minList):
                pointIndex = [i for i, j in enumerate(minList) if j == min(minList)]
                point = [i for i in intersect if i != None][pointIndex[0]]
                dots.append(pyglet.shapes.Circle(point.x, point.y, 5, color=(255,0,0), batch=batch, group=group))

        return dots

    def forward(self, forces):
        forces += Vector2D(100,0)
        self.reverse = False

    def backward(self, forces):
        forces += Vector2D(-100,0)
        self.reverse = True

    def left(self, forces, sidewayForce):
        forces += Vector2D(0,sidewayForce)

    def right(self, forces, sidewayForce):
        forces += Vector2D(0,-sidewayForce)

    def brake(self, forces):
        if self.reverse2 == False and (self.velocity.x > 2 or self.velocity.x < -2):
            forces += Vector2D(-150, 0)
        elif self.reverse2 == True and (self.velocity.x > 2 or self.velocity.x < -2):
            forces += Vector2D(150, 0)
        else:
            self.velocity.limit(0)
            self.reverse2 = False

    def update(self, dt, key, key_handler):
        forces = Vector2D(0,0)
        # self.intersection(lines)

        if self.velocity.x != 0:
            c = 100
            sigmoid = lambda x : 1 / (1 + math.e**-(x-c))

            sidewayForce = sigmoid(abs(self.velocity)) * 400
        else:
            sidewayForce = 0

        if key_handler[key.UP]:
            self.forward(forces)
        if key_handler[key.DOWN]:
            self.backward(forces)
        if key_handler[key.LEFT]:
            self.left(forces, sidewayForce)
        if key_handler[key.RIGHT]:
            self.right(forces, sidewayForce)
        if key_handler[key.SPACE]:
            self.brake(forces)

        velocityPrevious = self.velocity.copy()
        self.acceleration = forces.rotate(self.carRotation.rotation()) / self.mass
        self.acceleration.limit(100)
        self.velocity += self.acceleration * dt
        self.velocity.limit(200)
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
            self.rotation = self.carRotation.rotation()
        else:
            self.carRotation.rotate(180)
            self.velocity.limit(100)
            self.position += self.carRotation * -abs(self.velocity) * dt
            self.rotation = self.carRotation.rotation()
        self.middle = self.position + Vector2D(25, 15).rotate(self.rotation)

    def drive(self):
        self.test = 0
