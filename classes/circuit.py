from math import atan, sqrt
from classes.line import linline
from classes.Vector import Vector2D
import math
import pyglet

from typing import List

class circuit():
    def __init__(self, vertices: List[linline], checkpoints: List[linline]) -> None:
        self.vertices = vertices
        self.checkpoints = checkpoints
    
    @classmethod
    def fromSkeletonPoints(cls, points):
        vertices = cls.generate(points, 50)

    @classmethod
    def fromFullPoints(cls,points: List[List[Vector2D]], checkpoints: List[List[Vector2D]]) -> None:
        lines = []
        checkpoint = []
        margin = Vector2D(50,50)
        #Create a list of lines from the points
        for lane in points:
            for i in range(len(lane)):
                j = (i+1)%len(lane)
                lines.append(linline.fromPoints(lane[i]*60+margin,lane[j]*60+margin))
        
        for line in checkpoints:
            l = linline.fromPoints(line[0]*60+margin,line[1]*60+margin)
            l.color = (255,215,0)
            checkpoint.append(l)


        return cls(lines, checkpoint)

    def collidedWithCar(self, hitbox) -> bool:
        for line in self.vertices:
            for hitboxLine in hitbox:
                if line.intersect(hitboxLine) != None:
                    return True
        return False

    def draw(self, batch, screen, group):
        out = []
        for line in self.vertices:
            out.append(line.draw(batch, group, screen))
        
        for line in self.checkpoints:
            out.append(line.draw(batch, group, screen))

        return out

    def generate(self, points: list, width:int=100) -> List[linline]:
        r = width/2
        
        lines = []
        #Create a list of lines from the points
        for i in range(len(points)):
            j = (i+1)%len(points)
            lines.append(linline.fromPoints(points[i],points[j]))

        #Create paralel lines
        plines = lines[:]
        for line in lines:
            db = r/(math.sin(0.5*math.pi - math.atan(line.rc)))
            plines.append(linline(line.rc,line.b+db,line.limit,color=(255,0,0)))
            plines.append(linline(line.rc,line.b-db,line.limit,color=(0,0,255)))
            if(line.vertical):
                plines[-1].vertical = line.vertical
                plines[-1].limit = [i+r for i in line.limit]
                plines[-2].vertical = line.vertical
                plines[-2].limit = [i-r for i in line.limit]


        #Generate joint points
        """
        Define bissectrice P
        If snijpunt(bissectrice P, L1) == snijpunt(bissectrice P, L2):
            limit updaten
        """
        for i in range(len(lines)):
            j = (i+1)%len(lines)

            a = lines[i].rc
            c = lines[j].rc

            if(a+c != 0):
                yotta = (a*c - 1 + math.sqrt(a**2 + 1)*math.sqrt(c**2 + 1))/(a+c)
                yotta = -1/yotta
                rc = yotta
                b = points[j].y - yotta*points[j].x

                line = linline(rc,b,[points[j].x - 100,points[j].x + 100])
                print(line)
                plines.append(line)

        self.lines = plines


if __name__ == "main":
    # Testing
    window = pyglet.window.Window(resizable=True, fullscreen=True) 

    inner_points = [[18,3],[8,3],[5,4],[3,6],[2,9],[2,12],[3,14],[4,14],[6,12],[7,8],[8,7],[12,6],[16,6],[19,9],[20,11],[16,13],[13,12],[12,14],[13,15],[17,16],[20,15],[22,13],[23,8],[21,5]]
    inner = [Vector2D(i[0],i[1]) for i in inner_points]

    outer_points = [[18,0],[8,0],[2,3],[0,9],[0,14],[2,16],[5,16],[8,12],[9,9],[12,8],[15,8],[17,10],[16,11],[12,10],[11,11],[10,13],[10,15],[12,17],[17,17],[20,16],[23,14],[25,8],[23,4]]
    outer = [Vector2D(i[0],i[1]) for i in outer_points]


    circ = circuit.fromFullPoints([inner, outer])
    batch = pyglet.graphics.Batch()
    group = pyglet.graphics.OrderedGroup(0)
    running = True

    key = pyglet.window.key
    key_handler = key.KeyStateHandler()
    speed = 1.0

    @window.event
    def on_close():
        running = False

    @window.event
    def on_draw():
        render()

    def update(dt):
        pass

    def render():
        window.clear()
        _ = circ.draw(batch, window.get_size(), group)
        batch.draw()

    if __name__ == "__main__":
        pyglet.clock.schedule_interval(update, 1/120.0)
        pyglet.app.run()