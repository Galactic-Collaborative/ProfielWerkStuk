import pyglet
from classes.Vector import Vector2D

class Car():
    def __init__(self, x: int, y: int):
        self.position = Vector2D(x, y)
        self.acceleration = Vector2D(0,0)
        self.velocity = Vector2D(0,0)
        self.mass = 1
        self.rotation = 0
        self.reverse = False
        self.down = False

    def draw(self, batch):
        car = self.drawCar(batch)
        label = pyglet.text.Label(str(self.reverse), font_name='Times New Roman', font_size=36, x=80, y=1000, anchor_x='center', anchor_y='center')
        label.draw()
        return car

    def drawCar(self, batch):
        car = pyglet.sprite.Sprite(pyglet.resource.image('img/car.png'), x=self.position.x, y=self.position.y, batch=batch)
        car.scale = 0.5
        car.anchor_x = car.width // 2
        car.anchor_y = car.height // 2
        # car.rotation = -(self.velocity.rotation())
        car.rotation = -(self.rotation)
        return car

    def updateRotation(self):
        if self.reverse == False:
            self.rotation = self.velocity.rotation()
        else:
            self.rotation = 180 - self.velocity.rotation()

    def update(self, dt, key, key_handler):
        forces = Vector2D(0,0)
        if key_handler[key.UP]:
            if self.reverse == False:
                forces += Vector2D(100,0)
            else:
                forces += Vector2D(-100,0)
        if key_handler[key.DOWN]:
            self.down = True
        else: 
            self.down = False
        #     forces += Vector2D(-50,0)
        #     self.reverse = not self.reverse
        if key_handler[key.LEFT]:
            forces += Vector2D(0,100)
            # self.updateRotation()
        if key_handler[key.RIGHT]:
            forces += Vector2D(0,-100)
            # self.updateRotation()
        if key_handler[key.SPACE]:
            if self.velocity.x > 2:
                forces += Vector2D(-150, 0)
            elif self.velocity.x < -2:
                forces += Vector2D(-150, 0)
            # else:
            #     self.velocity.limit(0)

        if self.down == True:
            self.reverse = not self.reverse

        self.updateRotation()
        self.acceleration = forces.rotate(self.velocity.rotation()) / self.mass
        self.acceleration.limit(100)
        self.velocity += self.acceleration * dt
        self.velocity.limit(100)
        self.position += self.velocity * dt

    def drive(self):
        self.test = 0
