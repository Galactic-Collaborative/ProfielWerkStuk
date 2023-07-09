from __future__ import annotations
import math
from mathematics.shape import Shape
from mathematics.lines import Ray
from mathematics.vector import Vector2D

class Circle(Shape):
    radius : float

    def __init__(self, radius):
        self.radius = radius

    def intersect(self, center: Vector2D, ray: Ray) -> bool:
        """Check if a ray intersects with this circle

        Args:
            ray (Ray): The ray to check

        Returns:
            bool: True if the ray intersects with this circle
        """

        oc = ray.origin - center

        a = ray.direction @ ray.direction
        b = 2 * (oc @ ray.direction)
        c = oc @ oc - self.radius ** 2

        discriminant = b ** 2 - 4 * a * c

        if discriminant < 0:
            return False
        
        t1 = (-b + math.sqrt(discriminant)) / (2 * a)
        t2 = (-b - math.sqrt(discriminant)) / (2 * a)

        if t1 < 0 and t2 < 0:
            return False
        
        return True