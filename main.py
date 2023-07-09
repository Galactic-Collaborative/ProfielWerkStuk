from drawing.circuit_drawer import CircuitDrawer
from circuit import Circuit
from drawing.drawer import RenderOptions
import pyglet
import os

### MAIN LOOP
window = pyglet.window.Window(resizable=False, width=1920, height=1080, vsync=True)

dir_path = os.path.dirname(os.path.realpath(__file__))
path = dir_path + '/' + 'data/circuits/sigmaFalls.json'

batch = pyglet.graphics.Batch()

foreground = pyglet.graphics.Group(order=0)

options = RenderOptions(detailsOnly=False)

running = True

circuit = Circuit.from_json(path)

@window.event
def on_close():
    running = False

@window.event
def on_draw():
    render()

def update(dt):
    if not running:
        pyglet.app.exit()

def render():
    window.clear()

    draw_ref = CircuitDrawer(circuit).draw(batch, window, foreground, options)

    batch.draw()

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1/60.0)
    pyglet.app.run()