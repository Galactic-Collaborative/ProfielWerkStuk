from __future__ import annotations
from typing import List, NewType, Union, Type, Tuple
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
        self.r = Vector2D(a,-b)
        self.n = Vector2D(a,b)
        self.limit = limit
        self.color = color

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
        a = round(n.x,3)
        b = round(n.y,3)
        c = n @ point1
        
        limit = [point1.x, point2.x] if b != 0 else [point1.y, point2.y]
        return cls(a,b,c, limit=limit)

    def intersect(self, other, debug=False) -> Vector2D: # TODO
        """Calculate the point on which the two lines intersect
        
        The two lines intersect on one point. Intersect() calculates
        that point and give back a vector.

        Args:
            other: a linline; the line that intersects

        Returns:\n
        `Vector2D` A vector if a match is found \n
        `None` None if no match is found
        """
        #print((round(self.a,5) == round(self.b,5) and round(other.a,5) == round(other.b,5)) or (round(self.a,5) == -round(self.b,5) and round(other.a,5) == -round(other.b,5)))
        try: 
            if ((self.a == other.a) 
                or (self.b == 0 and other.b == 0) 
                or (round(self.a,5) == round(self.b,5) and round(other.a,5) == round(other.b,5)) 
                or (round(self.a,5) == -round(self.b,5) and round(other.a,5) == -round(other.b,5)) 
                or (self.b * other.a - self.a * other.b) == 0):#paralel lines
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
                if self._checkDomain(x,y,self,other):
                    return Vector2D(x,y)  
                else:
                    if debug: print("Domain Error")
                    return None
            else:
                if debugging: print('Something None')
                return None
        except ZeroDivisionError:
            print(f"self = {self}\nother = {other}")
            raise ZeroDivisionError()

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

    def getEndPoints(self) -> Tuple[Vector2D]:
        if self.b == 0:
            pointA = Vector2D(self.calcX(self.limit[0]), self.limit[0])
            pointB = Vector2D(self.calcX(self.limit[1]), self.limit[1])
        else:
            pointA = Vector2D(self.limit[0], self.calcY(self.limit[0]))
            pointB = Vector2D(self.limit[1], self.calcY(self.limit[1]))

        return (pointA, pointB)

    @staticmethod
    def _checkDomain(x: float, y: float, line1: linline, line2: linline) -> bool:
        collided: bool = False
        for line in [line1, line2]:
            if line.b==0:
                checkedVar = y
            else:
                checkedVar = x

            limit = sorted(line.limit)
            collided = (limit[0] <= checkedVar <= limit[1])
            if __name__ == "__main__":
                print(line1)
                print(line2)
                print(collided)
            
            if not collided: 
                break
        
        return collided


    def distance(self, point):
        # d = (abs(self.a * point.x + self.b * point.y - self.c))/math.sqrt(self.a**2 + self.b**2)
        # return d 
        d = (abs(self.n @ point - self.c))/abs(self.n)
        return d       
        
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
        return f"{self.a:.2f}x + {self.b:.2f}y = {self.c:.2f} {self.limit}"
    
    def __repr__(self):
        return f"linline({self.a}x + {self.b}y = {self.c} , limit={self.limit})"


if __name__ == "__main__":
    l1 = linline(0,-6,294)
    l2 = linline(-3,0,147)
    print(l1.intersect(l2))

    # l3 = linline.fromPoints((3,3),(8,13))
    # print(l2.intersect(l3))

