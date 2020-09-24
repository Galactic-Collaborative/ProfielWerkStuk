import pyglet
from classes.Vector import Vector2D

class Car():
    def __init__(self, x: int, y: int):
        self.position = Vector2D(x, y)
        self.acceleration = Vector2D(0,0)
        self.velocity = Vector2D(0,0)
        self.mass = 1
        self.rotation = 0
        self.limiet = 2
        self.limiet2 = -2

    def draw(self, batch):
        car = self.drawCar(batch)
        return car

    def drawCar(self, batch):
        car = pyglet.sprite.Sprite(pyglet.resource.image('classes/car.png'), x=self.position.x, y=self.position.y, batch=batch)
        car.scale = 0.5
        car.anchor_x = car.width // 2
        car.anchor_y = car.height // 2
        car.rotation = -(self.velocity.rotation())
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
            print("Space")
            if self.velocity.x != 0:
                print("Space2")
                forces += Vector2D(-150, 0)
            # if self.velocity.y != 0:
            #     print("Space3")
            #     forces += Vector2D(0, -150)
        
        self.acceleration = forces.rotate(self.velocity.rotation()) / self.mass
        self.acceleration.limit(100)
        self.velocity += self.acceleration * dt
        self.velocity.limit(100)
        self.position += self.velocity * dt
        
    def drive(self):
        self.test = 0
