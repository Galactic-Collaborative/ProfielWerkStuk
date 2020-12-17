from __future__ import annotations
from typing import List, NewType, Union, Type
import math
from pyglet import shapes

if __name__ == "__main__":
    debugging = True
else:
    debugging = False

if debugging:
    from Vector import Vector2D
else:
    from classes.Vector import Vector2D

class linline:
    """A mathematical representation of a linear line

    The linear line is a simplified version of the polynomial line 'polyline'.
    
    """
    def __init__(self, a: float, b: float, c:float, limit=[-math.inf,math.inf], color=(255,255,255)) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.r = Vector2D(a,b)
        self.limit = limit
        self.color = color
    
    """@classmethod
    def fromString(cls, string: str, variable="x"):
       ""
        DEPRECATED
        Create a line from a string

        The string has to be in the form of "ax+b".\n
        Change the variable with the second argument. Pass the variable as a string like 'p'.

       ""
        rc, b = string.split(variable)[:2]
        return cls(rc, b)
    """

    @classmethod
    def fromVector(cls, direction, location=Vector2D(0,0)):
        a = direction.y
        b = direction.x
        c = location.x * a + location.y * b
        return cls(a,b,c)
    
    @classmethod
    def fromPoints(cls, point1: Union[Vector2D, tuple], point2: Union[Vector2D, tuple]):
        """Create a line from points with a limited domain.

            Create a line from two vectors or tuples.
            The domain will be limited to the two points including.

            Args:
                a: `Vector2D | tuple` Point A of the line
                b: `Vector2D | tuple` Point B of the line

            Returns:
                `linline` A linear line with a limited domain.
        """
        if(type(point1) == tuple):
            point1 = Vector2D.fromTuple(point1)

        if(type(point2) == tuple):
            point2 = Vector2D.fromTuple(point2)

        r = point1 - point2
        n = r.toNormalVector()
        a = n.x
        b = n.y
        c = n @ point1
        
        limit = [point1.x, point2.x] if b != 0 else [point1.y, point2.y]
        return cls(a,b,c, limit=sorted(limit))

    def intersect(self, other) -> Vector2D: # TODO
        """Calculate the point on which the two lines intersect
        
        The two lines intersect on one point. Intersect() calculates
        that point and give back a vector.

        Args:
            other: a linline; the line that intersects

        Returns:\n
        `Vector2D` A vector if a match is found \n
        `None` None if no match is found
        """
        #print(f"self = {self}\nother = {other}") 
        if (self.a == other.a) or (self.b == 0 and other.b == 0) or (self.a == self.b and other.a == other.b) or (self.a == -self.b and other.a == -other.b):#paralel lines
            print('paralel!')
            return None

        if (self.a == 0 and other.b == 0) or (other.a == 0 and self.b == 0) == True: #lines with 90 degrees corners
            if self.a == 0:
                x = 1/other.a * other.c
                y = 1/self.b * self.c
                return Vector2D(x,y) if self._checkDomain(x,y,self,other) else None
            else:
                x = 1/self.a * self.c
                y = 1/other.b * other.c
                return Vector2D(x,y) if self._checkDomain(self.calcX(0),other.calcY(0),self,other) else None

        vertical = (self.b == 0 or other.b == 0)
        if not((self.b == 0 or other.b == 0)) and ((self.b * other.a - self.a * other.b) == 0):
            x = y = (other.c - (other.b*self.c)/self.b)/(other.a - (other.b*self.a)/self.b)
        elif self.b == 0 or other.b == 0:
            y = (self.c * other.a - self.a * other.c)/(self.b * other.a - self.a * other.b)
            x = self.calcX(y)
        else:
            x = (self.c * other.b - self.b * other.c)/(self.a * other.b - self.b * other.a)
            y = self.calcY(x)

        if not None in [x,y]:
            return Vector2D(x,y) if self._checkDomain(x,y,self,other) else None
        else:
            if debugging: print('Something None')
            return None

    def calc(self, x: float) -> float:
        """Calculate the output with a given x value

        The mathematical equivalent of f(x). Calc() calculates
        the value that corresponds to the x value given.

        Args:
            x: a float; the x value for the value to be calculated
        """
        return self.calcY(x)
    
    def calcX(self, y: float) -> Union[float, None]:
        if self.a != 0:
            result = (self.c - self.b * y)/(self.a)
        else: 
            result = None

        return result


    def calcY(self, x: float) -> Union[float, None]:
        if self.b != 0:
            result = (self.c - self.a * x)/(self.b)
        else: 
            result = None

        return result

    @staticmethod
    def _checkDomain(x: float, y: float, line1: linline, line2: linline) -> bool:
        collided: bool = False
        for line in [line1, line2]:
            if line.b==0:
                checkedVar = y
            else:
                checkedVar = x

            collided = (line.limit[0] <= checkedVar <= line.limit[1])
            if __name__ == "__main__":
                print(line1)
                print(line2)
                print(collided)
            
            if not collided: 
                break
        
        return collided


            
        

    def draw(self, batch, group, screen=[1920,1080], width=10):
        """Draw the line on the screen

        If the line is limited, it will draw the limited line in its whole.
        When the line is infinite, it will only draw the visible line.

        Args:
            screen: list containting ints; The width and height of the monitor in pixels.
        """

        if self.limit == [-math.inf,math.inf]:
            new_limit = [0,screen[0]]
            # if not (0<=self.calc(0)<=screen[1]):
            #     if(self.rc > 0):
            #         new_limit[0] = 0
            #     else:
            #         new_limit[0] = screen[0]
            
            # if not (0<=self.calc(screen[0])<=screen[1]):
            #     if(self.rc > 0):
            #         new_limit[0] = screen[0]
            #     else:
            #         new_limit[0] = 0
        else:
            new_limit = self.limit
        
        pos = new_limit
        if not self.b == 0:
            line = shapes.Line(pos[0], self.calcY(pos[0]), pos[1], self.calcY(pos[1]), width=width, color=self.color, batch=batch, group=group)
        else:
            line = shapes.Line(self.calcX(pos[0]), pos[0], self.calcX(pos[1]), pos[1], width=width, color=self.color, batch=batch, group=group)
        return line

    def __str__(self):
        return f"{self.a}x + {self.b}y = {self.c} {self.limit}"
    
    def __repr__(self):
        return f"linline({self.a}x + {self.b}y = {self.c} , limit={self.limit})"


if __name__ == "__main__":
    l1 = linline(0,-6,294)
    l2 = linline(-3,0,147)
    print(l1.intersect(l2))

    # l3 = linline.fromPoints((3,3),(8,13))
    # print(l2.intersect(l3))

