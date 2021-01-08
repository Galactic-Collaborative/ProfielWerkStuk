from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pyglet
import tensorflow as tf
import numpy as np

from tf_agents.environments import py_environment
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step as ts
from classes.car import Car
from classes.improvedCircuit import circuit
from classes.Vector import Vector2D

tf.compat.v1.enable_v2_behavior()

#HYPERPARAMETERS
dt = 1/60


class circuitEnv(py_environment.PyEnvironment):
    def __init__(self) -> None:
        self._action_spec = array_spec.BoundedArraySpec(
            shape=(), dtype=np.int32, minimum=0, maximum=3, name="action"
        )
        self._observation_spec = array_spec.BoundedArraySpec(
            shape=(8,), dtype=np.float32, minimum=0, name="observation"
        )

        self.circuit = circuit.fromJSON("circuits/BONK_CIRCUIT.json")
        self.agent = Car(self.circuit.startingPoint.x,self.circuit.startingPoint.y)
        self._episode_ended = False
        self.discount = 0.9925
        self.stepCountingCounter = 0

        self.viewer = None

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec
    
    def _reset(self):
        self.agent.reset()
        self.circuit.reset()

        self.agent.updateWithInstruction(dt, None)
        self.agent.mathIntersect(self.circuit.vertices)
        
        self.stepCountingCounter = 0
        self._episode_ended = False
        return ts.restart(self._observe())
    
    def _step(self, action):
        if self._episode_ended:
            print('episode ended')
            return self.reset()

        #run physics
        self.agent.updateWithInstruction(dt, action)
        hitbox = self.agent.generateHitbox()
        self.agent.mathIntersect(self.circuit.vertices)

        self.stepCountingCounter += 1;
        if self.circuit.collidedWithCar(hitbox):
            self._episode_ended = True
            return ts.termination(self._observe(), reward=-500.0)
        elif self.circuit.carCollidedWithCheckpoint(self.agent):
            reward = 300 * self.discount**self.stepCountingCounter
            return ts.transition(self._observe(),reward=reward)
        else:
            return ts.transition(self._observe(), reward=0)
    
    def _observe(self):
        return np.array(self.agent.observe(), dtype=np.float32)

    ### DRAWING STUFF ###
    def render(self, mode="human"):
        if self.viewer is None:
            self.viewer = Viewer(1920, 1080, self.agent, self.circuit)
        self.viewer.render()

class Viewer(pyglet.window.Window):
    color = {
        'background':"000000" 
    }

    def __init__(self, width, height, car, circuit):
        super(Viewer, self).__init__(width, height, resizable=False, caption='Machine Learning Car', vsync=True)

        self.batch = pyglet.graphics.Batch()

        self.car = car
        self.circuit = circuit

        self.layers = {
            "circuit": pyglet.graphics.OrderedGroup(0),
            "background": pyglet.graphics.OrderedGroup(1),
            "car": pyglet.graphics.OrderedGroup(2),
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
        for line in self.circuit.vertices:
            drawList.append(line.draw(self.batch, self.layers['circuit'], screen))
        
        drawList.append(self.circuit.checkpoints[self.circuit.currentCheckpoint - 1].draw(self.batch, self.layers['background'], screen))
        drawList.append(self.circuit.checkpoints[self.circuit.currentCheckpoint].draw(self.batch, self.layers['background'], screen))
        drawList.append(self.circuit.checkpoints[(self.circuit.currentCheckpoint + 1)%len(self.circuit.checkpoints)].draw(self.batch, self.layers['background'], screen))
        
        for point in self.car.circuitIntersections:
            drawList.append(pyglet.shapes.Circle(point.x, point.y, 5, color=(255,0,0), batch=self.batch, group=self.layers['background']))

        for line in self.car.generateLines():
            drawList.append(line.draw(self.batch, self.layers['background'], screen, 5))

        drawList.append(self.car.drawCar(self.batch, self.layers['car']))

        self.drawlist = drawList

    def on_draw(self):
        self.clear()
        self.batch.draw()
        




        
        
        


