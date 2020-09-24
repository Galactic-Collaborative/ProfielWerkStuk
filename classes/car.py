import pyglet
from Vector import Vector2D

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
        car = pyglet.sprite.Sprite(pyglet.resource.image('car.png'), x=self.position.x, y=self.position.y, batch=batch)
        car.scale = 0.5
        car.anchor_x = car.width // 2
        car.anchor_y = car.height // 2
        car.rotation = -(self.velocity.rotation())
        return car

    def update(self, dt, key_handler):
        forces = Vector2D(0,0)
        if key_handler[key.UP]:
            forces += Vector2D(100,0);
        if key_handler[key.DOWN]:
            forces += Vector2D(-100,0);
        if key_handler[key.LEFT]:
            forces += Vector2D(0,100);
        if key_handler[key.RIGHT]:
            forces += Vector2D(0,-100);
        
        self.acceleration = forces.rotate(self.velocity.rotation()) / self.mass
        self.acceleration.limit(100)
        self.velocity += self.acceleration * dt
        self.velocity.limit(100)
        self.position += self.velocity * dt
        
    def drive(self):
        self.test = 0

### MAIN LOOP
# config = pyglet.gl.Config(sample_buffers=1, samples=4)
window = pyglet.window.Window(resizable=True, fullscreen=False) 

car = Car(100,100)
batch = pyglet.graphics.Batch()
running = True

key = pyglet.window.key
key_handler = key.KeyStateHandler()
speed = 1.0

up_pressed = False
down_pressed = False
left_pressed = False
right_pressed = False

@window.event
def on_close():
    running = False

@window.event
def on_draw():
    render()

def update(dt):
    window.push_handlers(key_handler)
    if(running):
        car.update(dt, key_handler)
    else:
        pyglet.app.exit()

def render():
    window.clear()
    _ = car.draw(batch)
    batch.draw()

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1/120.0)
    pyglet.app.run()