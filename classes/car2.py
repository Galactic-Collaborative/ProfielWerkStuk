import pyglet
import math
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

    def draw(self, batch):
        car = self.drawCar(batch)
        return car

    def drawCar(self, batch):
        car = pyglet.sprite.Sprite(pyglet.resource.image('img/car.png'), x=self.position.x, y=self.position.y, batch=batch)
        car.scale = 0.5
        car.anchor_x = car.width // 2
        car.anchor_y = car.height // 2
        car.rotation = -(self.rotation)
        return car

    def eyes(self, batch):
        eyes = self.drawEyes(batch)
        return eyes

    def drawEyes(self, batch):
        lines = self.generateLines()
        out = []

        for line in lines:
            out.append(line.draw(batch))
        return out

    def generateLines(self):
        lines = []
        eyePoints = [Vector2D(i[0],i[1]) for i in self.eyesList]

        for line in eyePoints:
            secondLine = self.position + line.rotate(self.rotation)
            lines.append(linline.fromPoints(self.position, secondLine))
        return lines

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
        if self.reverse == False and (self.velocity.x > 2 or self.velocity.x < -2):
            forces += Vector2D(-150, 0)
        elif self.reverse == True and (self.velocity.x > 2 or self.velocity.x < -2):
            forces += Vector2D(150, 0)
        else:
            self.velocity.limit(0)

    def update(self, dt, key, key_handler):
        forces = Vector2D(0,0)

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
        
    def drive(self):
        self.test = 0
