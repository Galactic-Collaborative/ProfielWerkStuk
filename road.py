from __future__ import annotations
from mathematics.vector import Vector2D
from mathematics.lines import Ray, Line


class Road:
    """Represents a Road

        The Road is a list of lines. The lines are connected to each other.
    """
    lines : list[Line]

    def __init__(self, lines: list[Line]) -> None:
        self.lines = lines

    def Intersect(self, ray: Ray) -> Vector2D | None:
        """Calculate the intersection point of a ray with the circuit

        Args:
            ray: `Ray` The ray to intersect with

        Returns:
            `Vector2D | None` The intersection point or None if there is no intersection
        """
        intersections = [point for line in self.lines if (point := line.Intersect(ray)) is not None]
        distances = [(point - ray.origin).Length() for point in intersections]
        return intersections[distances.index(min(distances))] if len(distances) > 0 else None


    def IntersectAny(self, ray: Ray) -> bool:
        """Check if a ray intersects with the circuit

        Args:
            ray: `Ray` The ray to intersect with

        Returns:
            `bool` True if the ray intersects with the circuit
        """
        return any(line.Intersect(ray) is not None for line in self.lines)
