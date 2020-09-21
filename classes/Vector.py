import math
import typing
import numpy as np

# Typing
Vector2D = typing.NewType("Vector2D", object)

class Vector2D:
    """A mathematical representation of a 2-dimensional vector

    This vector can be used in many ways and is integrated with other representations
    such as Line.
    
    """
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
    

    @classmethod
    def fromTuple(cls, t: tuple):
        return cls(t[0], t[1])
    
    @classmethod
    def fromAngle(cls, angle):
        return cls(math.sin(angle), math.cos(angle))

    ### Normal Algebraic func
    def __add__(self, other: Vector2D) -> Vector2D:
        """Add two vectors together using the '+' operator

            ### Args:
                other: A vector.
        """
        if(type(other) == Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)


    def __sub__(self, other: Vector2D) -> Vector2D:
        """Subtract two vectors using the '-' operator

            ### Args:
                other: A vector.
        """
        if(type(other) == Vector2D):
            return Vector2D(self.x - other.x, self.y - other.y)


    def __mul__(self, other: float) -> Vector2D:
        """Multiply a vector using the '*' operator

            ### Args:
                other: A floating point.
        """
        if(isinstance(other, (int, float)) and not isinstance(other, bool)): #Check if other is a number
            return Vector2D(self.x * other, self.y * other);


    def __div__(self, other:int) -> Vector2D:
        """Divide a vector using the '/' operator

            ### Args:
                other: A floating point.
        """
        if(isinstance(other, (int, float)) and not isinstance(other, bool)): #Check if other is a number
            return Vector2D(self.x * 1/other, self.y * 1/other);

    def __matmul__(self, other: Vector2D) -> Vector2D:
        """Multiply the two vectors using the dot product method via python's '@' operator

            ### Explaination:
            Python 3.5 introduces the '@' operator, mainly for matrix multlipication.
            We use this feature to make our code pretier and more readable.

            ### Args:
                other: A vector.
        """
        if(type(other) == Vector2D):
            return self.x*other.x + self.y*other.y
        else:
            raise TypeError(f"Type of other vector is not valid: '{type(other).__name__}' is not a valid Vector2D");  
        
    ### Self Algebraic func
    def __iadd__(self, other: Vector2D) -> None:
        self.x += other.x
        self.y += other.y
        return self
    
    def __isub__(self, other: Vector2D) -> None:
        self.x -= other.x
        self.y -= other.y
        return self

    def __str__(self):
        return f"({self.x:.2f}, {self.y:.2f})"
    
    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"

    def __abs__(self):
        """The equivalent of | v | in mathematics

        Abs is the | | function and calculates the length of a vector
        using the Pythagorem Formula.

        Returns:
        `float` The length of the vector
        """
        return math.sqrt(self.x**2 + self.y**2)
    
    def dot(self, other: Vector2D):
        """Multiply the two vectors using the dot product method

        Multiply two vectors using the dot product.
        The dot product represents the length of a casted vector on another vector.

        Args: other - `vector` The vector to be multiplied.
        """
        if(type(other) == Vector2D):
            return self.x*other.x + self.y*other.y
        else:
            raise TypeError(f"Type of other vector is not valid: '{type(other).__name__}' is not a valid Vector2D");

    def rotation(self, other=None, degrees=True):
        """Calculate the rotation of one or two vectors

        The rotation is calculated with the vector (1,0)
        if other is None or omitted

        Args: other - _optional_ 'Vector'
        """
        if(type(other) == Vector2D):
            angle = math.acos((self @ other)/abs(self) * abs(other))
        elif(other == None):
            angle = math.atan2(self.y, self.x)
        else:
            raise TypeError(f"Type of other vector is not valid: '{type(other).__name__}' is not a valid Vector2D");

        if(degrees):
            return math.degrees(angle)
        else:
            return angle

    
    def limit(self, limit):
        """Limit the length of the vector

        The vector will be scaled to the given limit if it exceeds the limit.

        Args: limit - `int`
        """
        if abs(self) > limit:
            angle = self.rotation(degrees=False)
            x = math.cos(angle) * limit
            y = math.sin(angle) * limit
            self.x, self.y = x, y
        
        return self

### Testing###
if __name__ == "__main__":
    v1 = Vector2D(-1,-1)
    print(v1.rotation(degrees=True))

    v2 = Vector2D(1,-1)
    print(v2.rotation())

    v3 = Vector2D(2,2)
    v3 += v1;

    print(v3 * 2.0)
    print(v1.dot(v2))
    print(v1.dot(v1))
    print(v1 + v2)
    print(v2 - v1)
    print(abs(v1))

    v4 = Vector2D(0,6)
    v4.limit(5)
    print(v4)

    print(Vector2D(0,6).limit(5))
