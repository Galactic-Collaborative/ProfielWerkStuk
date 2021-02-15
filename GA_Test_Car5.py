import pyglet
import os
from classes.geneticAlgoritmNN.world import World
from classes.improvedCircuit import circuit
from classes.Vector import Vector2D
from pyglet import clock

class Viewer(pyglet.window.Window):
    color = {
        'background':"000000" 
    }

    def __init__(self, width, height, world, circuit):
        super(Viewer, self).__init__(width, height, resizable=False, caption='Genetic Algorithm Car Test', vsync=True)

        self.batch = pyglet.graphics.Batch()

        self.world = world
        self.circuit = circuit

        self.layers = {
            "circuitLayer": pyglet.graphics.OrderedGroup(0),
            "background": pyglet.graphics.OrderedGroup(1),
            "foreground": pyglet.graphics.OrderedGroup(2),
            "bestCarPlace": pyglet.graphics.OrderedGroup(3)
        }

    def render(self):
        self._prepare()
        self.switch_to()
        self.dispatch_events()
        self.dispatch_event('on_draw')
        self.flip()
    
    def _prepare(self):
        drawList = []
        screen = self.get_size()

        drawList.append(self.world.draw(self.batch, self.layers['foreground'], self.layers['background'], self.circuit.vertices))
        drawList.append(self.world.drawBestCarPlace(self.batch, self.layers['bestCarPlace']))
        drawList.append(self.circuit.draw(self.batch, screen, self.layers['circuitLayer'], hideAll=False))
        # drawList.append(self.world.drawBlindSpot(self.batch, self.layers['circuitLayer']))

        self.drawlist = drawList

    def on_draw(self):
        self.clear()
        self.batch.draw()

### MAIN LOOP
window_size = [1920, 1080]

dir_path = os.path.dirname(os.path.realpath(__file__))
path = dir_path + '/' + 'circuits/BONK_CIRCUIT_GACHECKPOINTS.json'
circ = circuit.fromJSON(path, window=window_size, method="fromFullPoints")
world = World(50, circ, window=window_size, load=False)
viewer = Viewer(window_size[0], window_size[1], world, circ)

running = True

key = pyglet.window.key
key_handler = key.KeyStateHandler()

def on_close():
    running = False

def on_draw():
    render()

def update(dt):
    viewer.push_handlers(key_handler)
    if(world.allCarsDead()):
        world.calcFitness()
        world.naturalSelection()
        world.crossParenting(4)
        world.mutateAll()
    else:
        carList = world.carList
        if world.load == True:
            for agent in carList:
                agent.nn.loadWeights()
                world.load = False
        if key_handler[key.S]:
            world.show = True
        if key_handler[key.H]:
            world.show = False
        if key_handler[key.B]:
            world.showA = False
        if key_handler[key.A]:
            world.showA = True
        if key_handler[key.T]:
            carList[0].nn.saveWeights()
            print("Best car is saved")
        if key_handler[key.K]:
            for agent in carList:
                agent.dead = True
        
        world.update(dt)

while running:
    update(1/60)
    viewer.render()
    viewer.push_handlers(key_handler)

    if key_handler[key.ESCAPE]:
        world.carList[0].nn.saveWeights()
        running = False
