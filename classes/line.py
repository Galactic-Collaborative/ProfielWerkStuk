from Vector import Vector2D
from typing import NewType, Union
import math

linline = NewType("linline", object)

class linline:
    """A mathematical representation of a linear line

    The linear line is a simplified version of the polynomial line 'polyline'.
    
    """
    def __init__(self, rc: float, b: float, limit=[-math.inf,math.inf]) -> None:
        self.rc = float(rc)
        self.b = float(b)
        self.limit = limit
    
    @classmethod
    def fromString(cls, string: str, variable="x") -> linline:
        """Create a line from a string

        The string has to be in the form of "ax+b".\n
        Change the variable with the second argument. Pass the variable as a string like 'p'.

        """
        rc, b = string.split(variable)[:2]
        return cls(rc, b)
    
    @classmethod
    def fromVector(cls, direction, location=Vector2D(0,0)):
        rc = direction.y / direction.x
        b = direction.x * location.y - direction.y * location.x
        return cls(rc, b)
    
    @classmethod
    def fromPoints(cls, a: Union[Vector2D, tuple], b: Union[Vector2D, tuple]) -> linline:
        """Create a line from points with a limited domain.

            Create a line from two vectors or tuples.
            The domain will be limited to the two points including.

            Args:
                a: `Vector2D | tuple` Point A of the line
                b: `Vector2D | tuple` Point B of the line

            Returns:
                `linline` A linear line with a limited domain.
        """
        if(type(a) == tuple):
            a = Vector2D.fromTuple(a)

        if(type(b) == tuple):
            b = Vector2D.fromTuple(b)
        
        rc = (b.y - a.y)/(b.x - a.x)
        p = a.y - rc * a.x
        limit = [a.x, b.x]

        return cls(rc, p, sorted(limit))

    def intersect(self, other: linline) -> Vector2D:
        """Calculate the point on which the two lines intersect
        
        The two lines intersect on one point. Intersect() calculates
        that point and give back a vector.

        Args:
            other: a linline; the line that intersects

        Returns:\n
        `Vector2D` A vector if a match is found \n
        `None` None if no match is found
        """
        new_x = (other.b - self.b) / (self.rc - other.rc)
        if self.limit[0] <= new_x <= self.limit[1] and other.limit[0] <= new_x <= other.limit[1]: 
            return Vector2D(new_x, self.calc(new_x))
        else:
            return None

    def calc(self, x: float) -> float:
        """Calculate the output with a given x value

        The mathematical equivalent of f(x). Calc() calculates
        the value that corresponds to the x value given.

        Args:
            x: a float; the x value for the value to be calculated
        """
        if(self.limit): #Check if the line is limited
            if not self.limit[0] <= x <= self.limit[1]: #Check if the domain contains the value of x
                raise ValueError(f"Domain Error: x value does not meet the domain ({self.limit})") 

        return self.rc * x + self.b

    def __str__(self):
        return f"Linear Line: {self.rc}x + {self.b} -> Limit: {self.limit}"
    
    def __repr__(self):
        return f"linline({self.rc}x + {self.b}, limit={self.limit})"

if __name__ == "__main__":
    l1 = linline(1,2, [1,3])
    l2 = linline.fromString("3x+1")
    print(l1)
    print(l2)
    print(l1.intersect(l2))

    l3 = linline.fromPoints((-2,-1),(3,1))
    print(l3.intersect(linline(1,0)))
    print(-math.inf <= -4 <= math.inf)

