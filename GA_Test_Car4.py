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
        drawList.append(self.world.drawBlindSpot(self.batch, self.layers['circuitLayer']))

        self.drawlist = drawList

    def on_draw(self):
        self.clear()
        self.batch.draw()

### MAIN LOOP
window = pyglet.window.Window(resizable=True, fullscreen=True)

checkpoints = [[[10,-1],[10,4]],[[4,1],[6,4]],[[13,5],[13,9]],[[15,-1],[15,4]]]
blindSpots = [[490,80],[220,210],[75,545],[100,850],[245,930],[375,850],[465,730],[485,485],[715,410],[925,415],[1130,645],[945,750],[720,645],[635,860],[735,975],[1000,985],[1180,935],[1330,820],[1425,500],[1300,280],[1070,90]]
indexSpot = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,0]
blindSpotPoints = [Vector2D(i[0],i[1]) for i in blindSpots]

circuit_checkpoints = []
for i, checkpoint in enumerate(checkpoints):
    circuit_checkpoints.append([])
    for point in checkpoint:
        circuit_checkpoints[i].append(Vector2D(point[0],point[1]))

dir_path = os.path.dirname(os.path.realpath(__file__))
path = dir_path + '/' + 'circuits/BONK_CIRCUIT_GACHECKPOINTS.json'
circ = circuit.fromJSON(path, window=window.get_size(), method="fromFullPoints")
world = World(50, circ.startingPoint.x, circ.startingPoint.y, window=window.get_size())
world.addBlindSpot(blindSpotPoints, indexSpot)
batch = pyglet.graphics.Batch()

running = True

key = pyglet.window.key
key_handler = key.KeyStateHandler()

checkpointNumber = len(circuit_checkpoints)

viewer = Viewer(1920, 1080, world, circ)

def on_close():
    running = False


def on_draw():
    render()

def update(dt):
    window.push_handlers(key_handler)
    if(world.allCarsDead()):
        world.calcFitness(circ.skeletonLines, checkpointNumber)
        world.naturalSelection()
        world.crossParenting(4)
        world.mutateAll()
    else:
        carList = world.carList
        if key_handler[key.S]:
            world.show = True
        if key_handler[key.H]:
            world.show = False
        if key_handler[key.B]:
            world.showA = False
        if key_handler[key.A]:
            world.showA = True
        if key_handler[key.T]:
            carList[world.bestCar].nn.saveWeights()
        if key_handler[key.K]:
            for agent in carList:
                agent.dead = True

        for agent in carList:
            hitbox = world.generateHitbox(agent)
            agent.car.currentCheckpoint = circ.carCollidedWithCheckpoint(agent.car)
            if circ.collidedWithCar(hitbox) == True:
                agent.dead = True
        
        world.update(dt, circ.vertices)

while True:
    update(1/60)
    viewer.render()
    window.push_handlers(key_handler)

    if key_handler[key.ESCAPE]:
        break
