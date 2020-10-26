import pyglet
from classes.Vector import Vector2D

class Car():
    def __init__(self, x: int, y: int):
        self.position = Vector2D(x, y)
        self.acceleration = Vector2D(0,0)
        self.velocity = Vector2D(0,0)
        self.mass = 1
        self.rotation = 0
        self.carRotation = Vector2D(0,0)

    def draw(self, batch):
        car = self.drawCar(batch)
        return car

    def drawCar(self, batch):
        car = pyglet.sprite.Sprite(pyglet.resource.image('img/car.png'), x=self.position.x, y=self.position.y, batch=batch)
        car.scale = 0.5
        car.anchor_x = car.width // 2
        car.anchor_y = car.height // 2
        # car.rotation = -(self.velocity.rotation())
        car.rotation = -(self.rotation)
        return car

    def update(self, dt, key, key_handler):
        forces = Vector2D(0,0)
        if key_handler[key.UP]:
            forces += Vector2D(100,0)
        if key_handler[key.DOWN]:
            forces += Vector2D(-100,0)
        if key_handler[key.LEFT]:
            forces += Vector2D(0,100)
        if key_handler[key.RIGHT]:
            forces += Vector2D(0,-100)
        if key_handler[key.SPACE]:
            if self.velocity.x > 2:
                forces += Vector2D(-150, 0)
            elif self.velocity.x < -2:
                forces += Vector2D(-150, 0)
            else:
                self.velocity.limit(0)
        
        self.acceleration = forces.rotate(self.carRotation.rotation()) / self.mass
        self.acceleration.limit(100)
        self.velocity += self.acceleration * dt
        self.velocity.limit(200)
        if self.velocity.x > 2 or self.velocity.x < -2:
            self.carRotation = self.velocity.copy()
            self.carRotation.normalize()
        self.position += self.carRotation * abs(self.velocity) * dt
        self.rotation = self.carRotation.rotation()
        

    def drive(self):
        self.test = 0
