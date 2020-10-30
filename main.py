import pyglet
from classes.car2 import Car
from classes.circuit import circuit
from classes.Vector import Vector2D

### MAIN LOOP
# config = pyglet.gl.Config(sample_buffers=1, samples=4)
window = pyglet.window.Window(resizable=True, fullscreen=True) 

inner_points = [[18,3],[8,3],[5,4],[3,6],[2,9],[2,12],[3,14],[4,14],[6,12],[7,8],[8,7],[12,6],[16,6],[19,9],[20,11],[16,13],[13,12],[12,14],[13,15],[17,16],[20,15],[22,13],[23,8],[21,5]]
inner = [Vector2D(i[0],i[1]) for i in inner_points]

outer_points = [[18,0],[8,0],[2,3],[0,9],[0,14],[2,16],[5,16],[8,12],[9,9],[12,8],[15,8],[17,10],[16,11],[12,10],[11,11],[10,13],[10,15],[12,17],[17,17],[20,16],[23,14],[25,8],[23,4]]
outer = [Vector2D(i[0],i[1]) for i in outer_points]

car = Car(200,200)
circ = circuit.fromFullPoints([inner, outer])

batch = pyglet.graphics.Batch()
running = True

key = pyglet.window.key
key_handler = key.KeyStateHandler()
speed = 1.0

@window.event
def on_close():
    running = False

@window.event
def on_draw():
    render()

def update(dt):
    window.push_handlers(key_handler)
    if(running):
        car.update(dt, key, key_handler)
    else:
        pyglet.app.exit()

def render():
    window.clear()
    _ = car.draw(batch)
    a = car.eyes(batch)
    b = circ.draw(batch, window.get_size())
    batch.draw()

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1/120.0)
    pyglet.app.run()