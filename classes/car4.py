import pyglet
from classes.Vector import Vector2D

class Car():
    def __init__(self, x: int, y: int):
        self.position = Vector2D(x, y)
        self.acceleration = 0
        self.velocity = 0
        self.mass = 1
        self.rotation = 0
        self.steerangle = 5
        self.velocity_scalar = 0

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

    def update(self, dt, key, key_handler):
        forces = Vector2D(0,0)
        if key_handler[key.UP]:
            forces += Vector2D(100,0)
        if key_handler[key.DOWN]:
            forces += Vector2D(-100,0)
        
        turn = 0
        if key_handler[key.LEFT]:
            turn = 1
        if key_handler[key.RIGHT]:
            turn = -1

        # if key_handler[key.SPACE]:
        #     if self.velocity.x > 2:
        #         forces += Vector2D(-150, 0)
        #     elif self.velocity.x < -2:
        #         forces += Vector2D(-150, 0)
            # else:
            #     self.velocity.limit(0)

        new_rotation = self.steerangle * turn
        self.rotation += new_rotation
        rotation_vector = Vector2D.fromAngle(90 - self.rotation)

        self.acceleration = abs(forces) / self.mass
        
        self.velocity_scalar += self.acceleration * dt
        self.velocity_vector = rotation_vector * self.velocity_scalar  
        self.velocity_vector.limit(100)
        self.position += self.velocity_vector * dt


    def drive(self):
        self.test = 0
