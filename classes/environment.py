from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import abc
import tensorflow as tf
import numpy as np

from tf_agents.environments import py_environment
from tf_agents.environments import tf_environment
from tf_agents.environments import tf_py_environment
from tf_agents.environments import utils
from tf_agents.specs import array_spec
from tf_agents.environments import wrappers
from tf_agents.environments import suite_gym
from tf_agents.trajectories import time_step as ts
from tf_agents.trajectories.time_step import transition

from classes.car import Car
from classes.circuit import Circuit
from classes.vector import Vector2D

tf.compat.v1.enable_v2_behavior()

inner_points = [[18,3],[8,3],[5,4],[3,6],[2,9],[2,12],[3,14],[4,14],[6,12],[7,8],[8,7],[12,6],[16,6],[19,9],[20,11],[16,13],[13,12],[12,14],[13,15],[17,16],[20,15],[22,13],[23,8],[21,5]]
outer_points = [[18,0],[8,0],[2,3],[0,9],[0,14],[2,16],[5,16],[8,12],[9,9],[12,8],[15,8],[17,10],[16,11],[12,10],[11,11],[10,13],[10,15],[12,17],[17,17],[20,16],[23,14],[25,8],[23,4]]
inner = [Vector2D(i[0],i[1]) for i in inner_points]
outer = [Vector2D(i[0],i[1]) for i in outer_points]


class circuitEnv(py_environment.PyEnvironment):
    def __init__(self) -> None:
        self._action_spec = array_spec.BoundedArraySpec(
            shape=(), dtype=np.int32, minimum=0, maximum=3, name="action"
        )
        self._observation_spec = array_spec.BoundedArraySpec(
            shape=(4,), dtype=np.float32, minimum=0, name="observation"
        )

        self.circuit = Circuit.fromFullPoints([inner, outer])
        self.agent = Car(0,0)
        self._episode_ended = False

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec
    
    def _reset(self):
        self.car.reset()
        self._episode_ended = False
        return ts.restart(np.array([self.state], dtype=np.int32))
    
    def _step(self, action):
        if self._episode_ended:
            return self.reset()

        if action == 0:
            self.car.forward()
        elif action == 1:
            self.car.backward()
        elif action == 2:
            self.car.left()
        elif action == 3:
            self.car.right()
        else:
            raise ValueError("`action` should be in range of 0 to 3")

        #run physics
        self.car.update()
        hitbox = self.car.generateHitbox()
        self.car.intersectEyes()

        if self.circuit.collidedWithCar(hitbox):
            self._episode_ended = True
            return ts.termination(np.array([]), reward=-2.0)
        elif self.car.collidedWithCheckpoint(hitbox):
            return ts.transition(self._observe(),reward=3.0, discount=1.0)
        else:
            return ts.transition(self._observe(), reward=1.0, discount=1.0)
    
    def _observe(self):
        return np.ndarray(self.car.observation)




        
        
        


