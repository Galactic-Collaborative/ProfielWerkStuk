from __future__ import annotations
from typing import List
import pyglet
import math
from .mathematics.lines import Ray
from .mathematics.vector import Vector2D
from .mathematics.shape import Shape


class RigidBody:
    """ A rigid body is a body that cannot change shape and can interact with other rigid bodies
    """
    position: Vector2D
    """ The position of the body
    """

    direction: Vector2D
    """ The direction of the body
    """

    shape: Shape
    """ The shape of the body """

    def __init__(self, position: Vector2D, direction: Vector2D, shape: Shape):
        self.position = position
        self.direction = direction
        self.shape = shape



class MovingBody(RigidBody):
    """A moving body with a mass, acceleration, velocity and position
    """
    mass : float
    acceleration : Vector2D
    velocity : Vector2D

    def __init__(self, position : Vector2D, mass : float = 1, shape: Shape = None):
        """Create a new moving body

        Args:
            position (Vector2D): The position of the body
            mass (float, optional): The mass of the body. Defaults to 1. Currently ignored
        """

        self.position = position
        self.mass = mass
        self.acceleration = Vector2D(0,0)
        self.velocity = Vector2D(0,0)
        super().__init__(position, self.velocity, shape)

    def update_location(self, dt: float):
        """Update the location of the body

        Args:
            dt (float): The time passed since the last update
        """
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt

class Car(MovingBody):
    """A car with a mass, acceleration, velocity and position
    """

    steering_angle : float
    """ The steering angle is the angle of the steering wheel
        This value is in radians and is between -PI and PI
    """

    motor_power: float
    throttle: float
    """ The throttle is the amount of power that is applied to the wheels
    """

    breaking: bool
    break_power: float
    """ The break power is the amount of power that is applied to the wheels
    """


    def __init__(self,
        position: Vector2D,
        motor_power: float = 1,
        mass : float = 1):
        super().__init__(position, mass)

        self.motor_power = motor_power
        self.steering_angle = 0

    def steer(self, delta_angle: float):
        self.steering_angle += delta_angle
        self.steering_angle = max(-math.pi, min(self.steering_angle, math.pi))

    def accelerate(self, throttle: float):
        self.breaking = False
        self.throttle = throttle

    def brake(self):
        self.breaking = True
        self.throttle = 0

    def update_location(self, dt: float):
        self.acceleration = Vector2D(0,0)

        # Calculate the acceleration
        self.acceleration += -(self.velocity * self.velocity) * 0.5
        power = self.motor_power * self.throttle

        rotation = self.velocity.rotation() + self.steering_angle
        steering_direction = Vector2D(math.cos(rotation), math.sin(rotation))
        self.acceleration += steering_direction * power

        super().update_location(dt)