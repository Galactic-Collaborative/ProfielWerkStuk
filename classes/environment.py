from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pyglet
import tensorflow as tf
import numpy as np

from tf_agents.environments import py_environment
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step as ts

if __name__ == "__main__":
    from classes.car import Car
    from classes.circuit import circuit
    from classes.Vector import Vector2D
else:
    from classes.car import Car
    from classes.circuit import circuit
    from classes.Vector import Vector2D

tf.compat.v1.enable_v2_behavior()

inner_points = [[18,3],[8,3],[5,4],[3,6],[2,9],[2,12],[3,14],[4,14],[6,12],[7,8],[8,7],[12,6],[16,6],[19,9],[20,11],[16,13],[13,12],[12,14],[13,15],[17,16],[20,15],[22,13],[23,8],[21,5]]
outer_points = [[18,0],[8,0],[2,3],[0,9],[0,14],[2,16],[5,16],[8,12],[9,9],[12,8],[15,8],[17,10],[16,11],[12,10],[11,11],[10,13],[10,15],[12,17],[17,17],[20,16],[23,14],[25,8],[23,4]]
inner = [Vector2D(i[0],i[1]) for i in inner_points]
outer = [Vector2D(i[0],i[1]) for i in outer_points]

checkpoints = [[[10,-1],[10,4]],[[4,1],[6,4]],[[0,6],[3,7]],[[-1,13],[3,12]],[[4,13],[7,15]],[[6,9],[10,11]],[[11,5],[12,9]],[[15,10],[18,7]],[[15,10],[14,13]],[[9,14],[13,13]],[[15,17],[16,15]],[[21,12],[24,15]],[[22,8],[25,6]],[[19,5],[20,1]],[[15,-1],[15,4]]]
circuit_checkpoints = []
for i, checkpoint in enumerate(checkpoints):
    circuit_checkpoints.append([])
    for x, point in enumerate(checkpoint):
        circuit_checkpoints[i].append(Vector2D(point[0],point[1]))

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

        self.circuit = circuit.fromFullPoints([inner, outer], circuit_checkpoints, Vector2D(12,1))
        self.agent = Car(self.circuit.startingPoint.x,self.circuit.startingPoint.y)
        self._episode_ended = False
        self.stepCountingVariableThatWillNotInterfere = 0

        self.batch = pyglet.graphics.Batch()


    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec
    
    def _reset(self):
        print(f"Resetting: round {self.stepCountingVariableThatWillNotInterfere}")
        self.stepCountingVariableThatWillNotInterfere += 1
        self.agent.reset()
        self.agent.updateWithInstruction(dt, None)
        self.agent.mathIntersect(self.circuit.vertices)

        self._episode_ended = False
        return ts.restart(self._observe())
    
    def _step(self, action):
        if self._episode_ended:
            return self.reset()

        #run physics
        self.agent.updateWithInstruction(dt, action)
        hitbox = self.agent.generateHitbox()
        self.agent.mathIntersect(self.circuit.vertices)

        if self.circuit.collidedWithCar(hitbox):
            self._episode_ended = True
            return ts.termination(self._observe(), reward=-2.0)
        elif self.circuit.carCollidedWithCheckpoint(self.agent):
            return ts.transition(self._observe(),reward=3.0, discount=1.0)
        else:
            return ts.transition(self._observe(), reward=1.0, discount=0.95)
    
    def _observe(self):
        return np.array(self.agent.observe(), dtype=np.float32)





    ### DRAWING STUFF ###

    def draw(self):
        layers = {
            "circuit": pyglet.graphics.OrderedGroup(0),
            "background": pyglet.graphics.OrderedGroup(1),
            "car": pyglet.graphics.OrderedGroup(2),
        }
        drawList = []
        drawList.append(self.agent.draw2(self.batch, layers))
        drawList.append(self.agent.intersectEyes(self.batch, self.circuit.vertices, layers['background']))
        drawList.append(self.circuit.draw(self.batch, [1920,1080], layers["circuit"]))



        
        
        


