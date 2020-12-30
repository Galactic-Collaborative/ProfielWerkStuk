import pyglet
from classes.car import Car
from classes.circuit import circuit
from classes.Vector import Vector2D

### MAIN LOOP
# config = pyglet.gl.Config(sample_buffers=1, samples=4)
window = pyglet.window.Window(resizable=True, fullscreen=True)

inner_points = [[18,3],[8,3],[5,4],[3,6],[2,9],[2,12],[3,14],[4,14],[6,12],[7,8],[8,7],[12,6],[16,6],[19,9],[20,11],[16,13],[13,12],[12,14],[13,15],[17,16],[20,15],[22,13],[23,8],[21,5]]
outer_points = [[18,0],[8,0],[2,3],[0,9],[0,14],[2,16],[5,16],[8,12],[9,9],[12,8],[15,8],[17,10],[16,11],[12,10],[11,11],[10,13],[10,15],[12,17],[17,17],[20,16],[23,14],[25,8],[23,4]]
inner = [Vector2D(i[0],i[1]) for i in inner_points]
outer = [Vector2D(i[0],i[1]) for i in outer_points]
checkpoints = [[[10,-1],[10,4]],[[4,1],[6,4]],[[0,6],[3,7]],[[-1,13],[3,12]],[[4,13],[7,15]],[[6,9],[10,11]],[[11,5],[12,9]],[[15,10],[18,7]],[[15,10],[14,13]],[[9,14],[13,13]],[[15,17],[16,15]],[[21,12],[24,15]],[[22,8],[25,6]],[[19,5],[20,1]],[[15,-1],[15,4]]]
circuit_checkpoints = []
for i, checkpoint in enumerate(checkpoints):
    circuit_checkpoints.append([])
    for point in checkpoint:
        circuit_checkpoints[i].append(Vector2D(point[0],point[1]))

circ = circuit.fromFullPoints([inner, outer], circuit_checkpoints, Vector2D(12,1), window=window.get_size())

car = Car(circ.startingPoint.x,circ.startingPoint.y)
car.position = circ.startingPoint

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
        circ.carCollidedWithCheckpoint(car)
        hitbox = car.generateHitbox()
        car.mathIntersect(circ.vertices)
        if circ.collidedWithCar(hitbox) == True:
            car.dead = True
            circ.reset()
            car.reset()
    else:
        pyglet.app.exit()

def render():
    window.clear()
    foreground = pyglet.graphics.OrderedGroup(2)
    background = pyglet.graphics.OrderedGroup(1)
    circuitLayer = pyglet.graphics.OrderedGroup(0)

    e = car.draw(batch, foreground)
    a = car.eyes(batch, background)
    b = circ.draw(batch, window.get_size(), circuitLayer)
    c = car.hitbox(batch, background)
    d = car.intersectEyes(batch, circ.vertices, background)
    batch.draw()

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1/120.0)
    pyglet.app.run()