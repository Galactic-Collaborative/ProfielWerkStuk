from __future__ import annotations
import math
from mathematics.shape import Shape
from mathematics.lines import Ray

class AABB(Shape):
    """An axis-aligned bounding box
    """
    x : float
    y : float
    width : float
    height : float

    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def intersect(self, ray: Ray) -> bool:
        """Check if a ray intersects with this box

        Args:
            ray (Ray): The ray to check

        Returns:
            bool: True if the ray intersects with this box
        """
        t1 = (self.x - ray.origin.x) / ray.direction.x
        t2 = (self.x + self.width - ray.origin.x) / ray.direction.x
        t3 = (self.y - ray.origin.y) / ray.direction.y
        t4 = (self.y + self.height - ray.origin.y) / ray.direction.y

        tmin = max(min(t1, t2), min(t3, t4))
        tmax = min(max(t1, t2), max(t3, t4))

        if tmax < 0 or tmin > tmax:
            return False
        
        return True