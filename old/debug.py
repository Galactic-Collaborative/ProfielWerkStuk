from classes.improvedLine import linline
from classes.Vector import Vector2D

l3 = linline.fromPoints(Vector2D(1,1), Vector2D(5,5))
print(l3.getEndPoints())