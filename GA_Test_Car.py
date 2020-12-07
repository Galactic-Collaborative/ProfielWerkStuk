import pyglet
from classes.geneticAlgoritm.world import World

running = True

### MAIN LOOP
window = pyglet.window.Window(resizable=True, fullscreen=True)

world = World(100, window=window.get_size())
batch = pyglet.graphics.Batch()
running = True

@window.event
def on_close():
    running = False

@window.event
def on_draw():
    render()

def update(dt):
    if(world.allCarsDead()):
        world.calcFitness()
        world.naturalSelection()
        world.mutateAll()
    else:
        world.update(dt)

def render():
    window.clear()
    foreground = pyglet.graphics.OrderedGroup(0)
    carDrawings = world.draw(batch, foreground)
    goal = pyglet.shapes.Circle(window.get_size()[0]-10, window.get_size()[1]-10, 10, color=(0,255,0), batch=batch)
    batch.draw()

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1/120.0)
    pyglet.app.run()