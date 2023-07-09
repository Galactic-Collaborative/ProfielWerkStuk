from __future__ import annotations
import math
from typing import Tuple

class Vector2D:
    """A mathematical representation of a 2-dimensional vector
    This vector can be used in many ways and is integrated with other representations
    such as Line.

    """

    x: float
    y: float

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    @classmethod
    def fromTuple(cls, t: Tuple[float, float]):
        return cls(t[0], t[1])

    @classmethod
    def fromAngle(cls, angle: float):
        return cls(math.sin(angle), math.cos(angle))

    ### Normal Algebraic func
    def __add__(self, other: Vector2D) -> Vector2D:
        """Add two vectors together using the '+' operator
            ### Args:
                other: A vector.
        """
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2D) -> Vector2D:
        """Subtract two vectors using the '-' operator
            ### Args:
                other: A vector.
        """
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float | Vector2D) -> Vector2D:
        """Multiply a vector using the '*' operator
            ### Args:
                other: A floating point.
        """

        if(type(other) == Vector2D):
            return Vector2D(self.x * other.x, self.y * other.y)
        if(type(other) == float):
            return Vector2D(self.x * other, self.y * other)

        raise TypeError(f"Cannot multiply Vector2D with {type(other)}")


    def __truediv__(self, other:float) -> Vector2D:
        """Divide a vector using the '/' operator
            ### Args:
                other: A floating point.
        """
        return self * (1/other)

    def __matmul__(self, other: Vector2D) -> float:
        """Multiply the two vectors using the dot product method via python's '@' operator
            ### Explanation:
            Python 3.5 introduces the '@' operator, mainly for matrix multlipication.
            We use this feature to make our code pretier and more readable.
            ### Args:
                other: A vector.
        """
        return self.x*other.x + self.y*other.y

    def __iadd__(self, other: Vector2D):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other: Vector2D):
        self.x -= other.x
        self.y -= other.y
        return self

    def __str__(self):
        return f"({self.x:.2f}, {self.y:.2f})"

    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"

    def __abs__(self):
        """Calculate the length of the vector
        The length is calculated using the pythagorean theorem.
        """
        return math.sqrt(self.x**2 + self.y**2)

    def __neg__(self) -> Vector2D:
        return Vector2D(-self.x, -self.y)

    def __eq__(self, other: Vector2D) -> bool:
        return self.x == other.x and self.y == other.y

    def dot(self, other: Vector2D) -> float:
        """Multiply the two vectors using the dot product method
        Multiply two vectors using the dot product.
        The dot product represents the length of a cast vector on another vector.
        Args: other - `vector` The vector to be multiplied.
        """
        return self.x*other.x + self.y*other.y

    def length(self) -> float:
        return abs(self);

    def rotation(self, other: Vector2D | None=None) -> float:
        """Calculate the rotation of one or two vectors
        The rotation is calculated with the vector (1,0)
        if other is None or omitted
        Args: other - _optional_ 'Vector'
        """
        if(type(other) == Vector2D):
            var: float = self @ other / abs(self) * abs(other);# type: ignore
            angle = math.acos(var)
        else:
            angle = math.atan2(self.y, self.x)

        return angle

    def rotate(self, rotation: float) -> Vector2D:
        """Rotate the vector

        The vector is rotated by the given rotation.

        Args: rotation - `float | int` rotation in radians
        """

        x2 = math.cos(rotation) * self.x - math.sin(rotation) * self.y
        y2 = math.sin(rotation) * self.x + math.cos(rotation) * self.y

        return Vector2D(x2,y2)

    def perpendicular(self) -> Vector2D:
        """Calculate the perpendicular vector

        The perpendicular vector is calculated by swapping the x and y values and
        multiplying the new x value with -1.
        """
        return Vector2D(-self.y, self.x)

    def limit(self, limit: float) -> Vector2D:
        """Limit the length of the vector

        The vector will be scaled to the given limit if it exceeds the limit.
        """
        if abs(self) > limit:
            angle = self.rotation()
            x = math.cos(angle) * limit
            y = math.sin(angle) * limit
            self.x, self.y = x, y

        return self

    def normalized(self) -> Vector2D:
        """Normalize the vector"""
        if abs(self) != 0:
            new_self = self / abs(self)
            return new_self
        else:
            return self

    def copy(self):
        return Vector2D(self.x, self.y)

    def lerp(self, other: Vector2D, t: float):
        return self * (1-t) + other * t


### Testing###
if __name__ == "__main__":
    # v1 = Vector2D(-1,-1)
    # print(v1.rotation(degrees=True))

    v2 = Vector2D(1,2)
    # print(v2.rotation())

    v3 = Vector2D(2,3)

    # v4 = Vector2D(0,6)
    # v4.limit(5)
    # print(v4)

    # print(Vector2D(0,6).limit(5))

    # v5 = Vector2D(5,5)
    # print(v5.rotate(90))


    v2.normalized()
    print(f"V2 normalize:{v2}")
    print(f"V3 normalize:{v3.normalized()}")
    d = v2.dot(v3)
    print(d)

    print(Vector2D(1,0) == Vector2D(1,0))
    v5 = Vector2D(5,1)
    print(v5.rotate(90))
