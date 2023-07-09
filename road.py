from __future__ import annotations
from mathematics.vector import Vector2D
from mathematics.lines import BoundedLine, Ray, Line


class Road:
    """Represents a Road

        The Road is a list of lines. The lines are connected to each other.
    """
    left : list[BoundedLine]
    right: list[BoundedLine]

    whole: list[BoundedLine]

    def __init__(self, left: list[BoundedLine], right: list[BoundedLine]):
        """Create a new Road

        Args:
            left (list[Line]): The left lines of the road
            right (list[Line]): The right lines of the road
        """
        self.left = left
        self.right = right

        self.whole = left + right

    def intersect(self, ray: Ray) -> Vector2D | None:
        """Calculate the intersection point of a ray with the circuit

        Args:
            ray: `Ray` The ray to intersect with

        Returns:
            `Vector2D | None` The intersection point or None if there is no intersection
        """
        intersections = [point for line in self.whole if (point := line.intersect(ray)) is not None]
        distances = [(point - ray.origin).length() for point in intersections]
        return intersections[distances.index(min(distances))] if len(distances) > 0 else None


    def intersect_any(self, ray: Ray) -> bool:
        """Check if a ray intersects with the circuit

        Args:
            ray: `Ray` The ray to intersect with

        Returns:
            `bool` True if the ray intersects with the circuit
        """
        return any(line.intersect(ray) is not None for line in self.whole)
