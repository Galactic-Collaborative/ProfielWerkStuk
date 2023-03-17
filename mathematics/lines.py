from __future__ import annotations
from mathematics.vector import Vector2D

class Ray:
    direction : Vector2D
    origin : Vector2D

    def __init__(self, direction: Vector2D, origin: Vector2D) -> None:
        self.direction = direction
        self.origin = origin

    def __repr__(self) -> str:
        return f"Ray({self.direction}, {self.origin})"

    def Calc(self, t: float) -> Vector2D:
        if t < 0: raise ValueError("t must be positive")
        return self.origin + self.direction * t

class Line:
    direction : Vector2D
    origin : Vector2D

    def __init__(self, direction: Vector2D, origin: Vector2D) -> None:
        self.direction = direction
        self.origin = origin

    def __repr__(self) -> str:
        return f"Line({self.direction}, {self.origin})"

    @classmethod
    def FromPoints(cls, a: Vector2D, b: Vector2D) -> Line:
        """Create a line from two points

        Args:
            a (Vector2D): The first point
            b (Vector2D): The second point

        Returns:
            Line: The line through the two given points
        """
        direction = b - a
        return cls(direction, a)

    def Intersect(self, ray: Ray) -> Vector2D | None:
        """Calculate the intersection point of two lines

        Args:
            ray: `Ray` The ray to intersect with

        Returns:
            `Vector2D | None` The intersection point or None if there is no intersection
        """
        n = self.direction @ ray.direction
        if n == 0:
            return None

        diff = ray.origin - self.origin
        t = (diff @ ray.direction) / n

        return self.Calc(t)

    def Distance(self, point: Vector2D) -> float:
        """Calculate the distance between a line and a point

        Args:
            point (Vector2D): The point to calculate the distance to

        Returns:
            float: The distance between the line and the point
        """
        return abs((point - self.origin) @ self.direction.Perpendicular())

    def Calc(self, t: float) -> Vector2D:
        return self.origin + self.direction * t

class BoundedLine(Line):
    length : float

    __endPoint : Vector2D;

    def __init__(self, direction: Vector2D, origin: Vector2D, length:float) -> None:
        super().__init__(direction, origin)
        self.length = length
        __endPoint = origin + direction * length;

    @classmethod
    def FromPoints(cls, a: Vector2D, b: Vector2D) -> BoundedLine:
        """Create a line from two points

        Args:
            a (Vector2D): The first point
            b (Vector2D): The second point

        Returns:
            BoundedLine: The line between the two given points
        """
        direction = b - a
        return cls(direction, a, direction.Length())

    def Intersect(self, ray: Ray) -> Vector2D | None:
        """Calculate the intersection point of two lines

        Args:
            ray: `Ray` The ray to intersect with

        Returns:
            `Vector2D | None` The intersection point or None if there is no intersection
        """
        intersection = super().Intersect(ray);

        # If there is no intersection, return None
        if (intersection is None):
            return None;

        # If the intersection is within the bounds of the line, return the intersection
        if(intersection - self.origin).Length() <= self.length:
            return intersection

        # Otherwise, return None
        return None;

    def Distance(self, point: Vector2D) -> float:
        """Calculate the distance between a line and a point, taken into account the bounds of the line

        Args:
            point (Vector2D): The point to calculate the distance to

        Returns:
            float: The distance between the line and the point
        """

        # Calculate the point on the line closest to the given point
        t = (point - self.origin) @ self.direction;

        if t < 0:
            return (point - self.origin).Length();
        elif t > self.length:
            return (point - self.__endPoint).Length();
        else:
            return super().Distance(point);

    def __repr__(self) -> str:
        return f"BoundedLine({self.direction}, {self.origin}, {self.length})"

    def Calc(self, t: float) -> Vector2D:
        """Calculate the point on the line at a given distance

        Args:
            t (float): The distance along the line

        Raises:
            ValueError: If t is out of bounds

        Returns:
            Vector2D: The point on the line at the given distance
        """
        if t <= self.length:
            return super().Calc(t)
        else: raise ValueError("t is out of bounds");