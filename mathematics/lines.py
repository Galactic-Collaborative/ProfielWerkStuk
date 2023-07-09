from __future__ import annotations

if(__name__ == "__main__"):
    from vector import Vector2D
else:
    from mathematics.vector import Vector2D

class Ray:
    direction : Vector2D
    origin : Vector2D

    def __init__(self, origin: Vector2D, direction: Vector2D) -> None:
        self.direction = direction
        self.origin = origin

    def __repr__(self) -> str:
        return f"Ray({self.direction}, {self.origin})"

    def calc(self, t: float) -> Vector2D:
        if t < 0: raise ValueError("t must be positive")
        return self.origin + self.direction * t

class Line:
    direction : Vector2D
    origin : Vector2D

    def __init__(self, origin: Vector2D, direction: Vector2D) -> None:
        self.origin = origin
        self.direction = direction.normalized()

    def __repr__(self) -> str:
        return f"Line(origin={self.origin}, direction={self.direction})"

    @classmethod
    def from_points(cls, a: Vector2D, b: Vector2D) -> Line:
        """Create a line from two points

        Args:
            a (Vector2D): The first point
            b (Vector2D): The second point

        Returns:
            Line: The line through the two given points
        """
        direction = b - a
        return cls(a, direction)

    def intersect(self, ray: Ray) -> Vector2D | None:
        """Calculate the intersection point of two lines

        Args:
            ray: `Ray` The ray to intersect with

        Returns:
            `Vector2D | None` The intersection point or None if there is no intersection
        """
        n = ray.direction.perpendicular()
        p = self.direction @ n
        if p == 0:
            return None

        diff = ray.origin - self.origin
        t = (diff @ n) / p

        return self.calc(t)

    def distance(self, point: Vector2D) -> float:
        """Calculate the distance between a line and a point

        Args:
            point (Vector2D): The point to calculate the distance to

        Returns:
            float: The distance between the line and the point
        """
        return abs((point - self.origin) @ self.direction.perpendicular())

    def calc(self, t: float) -> Vector2D:
        return self.origin + self.direction * t

class BoundedLine(Line):
    length : float

    __endPoint : Vector2D;

    def __init__(self, origin: Vector2D, direction: Vector2D, length:float) -> None:
        super().__init__(origin, direction)
        self.length = length
        __endPoint = origin + self.direction * length;

    @classmethod
    def from_points(cls, a: Vector2D, b: Vector2D) -> BoundedLine:
        """Create a line from two points

        Args:
            a (Vector2D): The first point
            b (Vector2D): The second point

        Returns:
            BoundedLine: The line between the two given points
        """
        direction = b - a
        return cls(a, direction, direction.length())

    def intersect(self, ray: Ray) -> Vector2D | None:
        """Calculate the intersection point of two lines

        Args:
            ray: `Ray` The ray to intersect with

        Returns:
            `Vector2D | None` The intersection point or None if there is no intersection
        """
        intersection = super().intersect(ray);

        # If there is no intersection, return None
        if (intersection is None):
            return None;

        # If the intersection is within the bounds of the line, return the intersection
        if (intersection - self.origin).normalized() == self.direction and (intersection - self.origin).length() <= self.length:
            return intersection

        # Otherwise, return None
        return None;

    def distance(self, point: Vector2D) -> float:
        """Calculate the distance between a line and a point, taken into account the bounds of the line

        Args:
            point (Vector2D): The point to calculate the distance to

        Returns:
            float: The distance between the line and the point
        """

        # Calculate the point on the line closest to the given point
        t = (point - self.origin) @ self.direction;

        if t < 0:
            return (point - self.origin).length();
        elif t > self.length:
            return (point - self.__endPoint).length();
        else:
            return super().distance(point);

    def __repr__(self) -> str:
        return f"BoundedLine(origin={self.origin},direction={self.direction},length={self.length})"

    def calc(self, t: float) -> Vector2D:
        """Calculate the point on the line at a given distance

        Args:
            t (float): The distance along the line

        Raises:
            ValueError: If t is out of bounds

        Returns:
            Vector2D: The point on the line at the given distance
        """
        if t <= self.length:
            return super().calc(t)
        else: raise ValueError("t is out of bounds");



if(__name__ == "__main__"):
    # Test the Line class
    line = Line.from_points(Vector2D(0, 0), Vector2D(1, 1))

    print(line)

    print(line.intersect(Ray(Vector2D(0, 1), Vector2D(1, 0))))

    print(line.distance(Vector2D(0, 1)))

    print(line.calc(1))

    # Test the BoundedLine class
    boundedLine = BoundedLine.from_points(Vector2D(0, 0), Vector2D(1, 1))

    print(boundedLine)

    print(boundedLine.intersect(Ray(Vector2D(0, 0.5), Vector2D(1, 0))))

    print(boundedLine.distance(Vector2D(0, 1)))

    print(boundedLine.calc(1))