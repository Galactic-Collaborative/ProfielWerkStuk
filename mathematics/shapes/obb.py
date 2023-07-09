from __future__ import annotations
import math
from mathematics.shape import Shape
from mathematics.lines import Ray

class OBB(Shape):
    """An oriented bounding box
    """
    x : float
    y : float
    width : float
    height : float
    angle : float

    def __init__(self, x: float, y: float, width: float, height: float, angle: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle

    def intersect(self, ray: Ray) -> bool:
        """Check if a ray intersects with this box

        Args:
            ray (Ray): The ray to check

        Returns:
            bool: True if the ray intersects with this box
        """

        raise NotImplementedError