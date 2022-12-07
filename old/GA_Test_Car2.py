import pyglet
import os
from classes.geneticAlgoritmNN.world import World
from classes.improvedCircuit import circuit
from classes.Vector import Vector2D
from pyglet import clock

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

@window.event
def on_close():
    running = False

@window.event
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

def render():
    window.clear()

    bestCarPlace = pyglet.graphics.OrderedGroup(3)
    foreground = pyglet.graphics.OrderedGroup(2)
    background = pyglet.graphics.OrderedGroup(1)
    circuitLayer = pyglet.graphics.OrderedGroup(0)

    carDrawings = world.draw(batch, foreground, background, circ.vertices)
    bestCarDrawing = world.drawBestCarPlace(batch, bestCarPlace)
    circuitDraw = circ.draw(batch, window.get_size(), circuitLayer, hideAll=False)
    blindSpotDraw = world.drawBlindSpot(batch, circuitLayer)
    batch.draw()

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, .140)
    pyglet.app.run()