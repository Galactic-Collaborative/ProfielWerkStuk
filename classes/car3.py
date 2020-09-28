import pyglet
from classes.Vector import Vector2D

class Car():
    def __init__(self, x: int, y: int):
        self.position = Vector2D(x, y)
        self.acceleration = Vector2D(0,0)
        self.velocity = Vector2D(0,0)
        self.mass = 1
        self.rotation = 0
        self.wheel_base = 70

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
            # else:
            #     self.velocity.limit(0)

        self.acceleration = forces.rotate(self.velocity.rotation()) / self.mass
        self.acceleration.limit(100)
        print(f"Acceleration: {self.acceleration}")

        self.rear_wheel = self.position.copy()
        self.front_wheel = self.position.copy()

        self.rear_wheel.x = self.rear_wheel.x - self.rear_wheel.x * (self.wheel_base / 2)
        self.front_wheel.x = self.front_wheel.x + self.front_wheel.x * (self.wheel_base / 2)
        self.rear_wheel += self.velocity * dt
        self.front_wheel += self.velocity.rotate(self.velocity.rotation()) * dt
        self.new_heading = (self.front_wheel - self.rear_wheel).normalize()
        print(f"New heading: {self.new_heading}")
        print(f"Velocity normalized: {self.velocity.normalize(in_place=False)}")
        self.d = self.new_heading.dot(self.velocity.normalize(in_place=False))
        print(f"Self d: {self.d}")
        if self.d > 0:
            self.velocity += self.acceleration * dt
        if self.d < 0:
            self.velocity -= self.acceleration * dt

        self.velocity.limit(100)
        print(f"Velocity: {self.velocity}")
        print(f"PositionBefore: {self.position}")
        self.position += self.velocity * dt
        print(f"PositionAfter: {self.position}")
        self.rotation = self.new_heading.rotation()
        print(" ")

    def drive(self):
        self.test = 0
