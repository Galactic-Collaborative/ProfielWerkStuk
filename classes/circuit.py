from math import atan, sqrt
if __name__ == "__main__":
    from improvedLine import linline
    from Vector import Vector2D
else:
    from classes.improvedLine import linline
    from classes.Vector import Vector2D

import math
import pyglet

from typing import List

class circuit():
    def __init__(self, vertices: List[linline], checkpoints: List[linline], startingPoint=Vector2D(0,0), monocar: bool=True) -> None:
        self.vertices = vertices
        self.checkpoints = checkpoints

        self.currentCheckpoint = 0

        self.startingPoint = startingPoint
        self.monocar = monocar    
    @classmethod
    def fromSkeletonPoints(cls, points, startingPoint=Vector2D(0,0)):
        vertices, checkpoints = cls.generate(points, 100)
        return cls(vertices, checkpoints, startingPoint)


    @classmethod
    def fromFullPoints(cls,points: List[List[Vector2D]], checkpoints: List[List[Vector2D]], startingPoint=Vector2D(0,0), window=(1820,1080), monocar: bool=True) -> None:
        lines = []
        checkpoint = []
        margin = Vector2D(50,50)
        max_x = max([p.x for p in points[0]])
        max_y = max([p.x for p in points[0]])
        scale = min((window[0]/max_x, window[1]/max_y))
        startPoint = startingPoint*scale + margin

        #Create a list of lines from the points
        for lane in points:
            for i in range(len(lane)):
                j = (i+1)%len(lane)
                lines.append(linline.fromPoints(lane[i]*scale+margin,lane[j]*scale+margin))
        
        for line in checkpoints:
            l = linline.fromPoints(line[0]*scale+margin,line[1]*scale+margin)
            l.color = (255,215,0)
            checkpoint.append(l)


        return cls(lines, checkpoint, startingPoint=startPoint, monocar=monocar)

    def collidedWithCar(self, hitbox) -> bool:
        for line in self.vertices:
            for hitboxLine in hitbox:
                if line.intersect(hitboxLine) != None:
                    return True
        return False

    def carCollidedWithCheckpoint(self, car) -> bool:
        currentCheckpoint = car.currentCheckpoint
        for line in car.generateHitbox():
            if self.checkpoints[currentCheckpoint].intersect(line) != None:
                currentCheckpoint = self.spawnNextCheckpoint(currentCheckpoint)

        self.currentCheckpoint = car.currentCheckpoint = currentCheckpoint
        return car.currentCheckpoint

    def spawnNextCheckpoint(self, currentCheckpoint):
        currentCheckpoint = (currentCheckpoint + 1)%len(self.checkpoints)
        return currentCheckpoint

    def draw(self, batch, screen, group):
        out = []
        for line in self.vertices:
            out.append(line.draw(batch, group, screen))
        
        if self.monocar:
            out.append(self.checkpoints[(self.currentCheckpoint + (len(self.checkpoints) - 1))%len(self.checkpoints)].draw(batch, group, screen))
            out.append(self.checkpoints[self.currentCheckpoint].draw(batch, group, screen))
            out.append(self.checkpoints[(self.currentCheckpoint + 1)%len(self.checkpoints)].draw(batch, group, screen))

        return out
    
    @staticmethod
    def generate(points: list, width:int=100) -> List[linline]:
        r = width/2
        
        lines = []
        directions = []
        #Create a list of lines from the points
        for i in range(len(points)):
            j = (i+1)%len(points)
            lines.append(linline.fromPoints(points[i],points[j]))
            directions.append(points[j] - points[i])

        print(lines)
        #Create paralel lines
        plines = lines[:]
        paralel_lines = [[],[]]
        for i, direction in enumerate(directions):
            normal_vector = direction.toNormalVector()/abs(direction) * r
            # w1 = points[i] + normal_vector
            # w2 = points[i] - normal_vector
            # c1 = lines[i].r @ w1
            # c2 = lines[i].r @ w2
            # paralel_lines[1].append(linline(lines[i].a, lines[i].b, c1))
            # paralel_lines[2].append(linline(lines[i].a, lines[i].b, c2))

            for j in range(2):
                w = points[i] + normal_vector*(-1)**(j+1)
                c = lines[i].r @ w
                paralel_lines[j].append(linline(lines[i].a, lines[i].b, c))


        print(paralel_lines)
        #Generate joint points
        for ring in paralel_lines:
            intersections = []
            intersections.append(ring[0].intersect(ring[1]))
            for i in range(1,len(ring)):
                j = (i+1)%len(ring)
                intersection = ring[i].intersect(ring[j])
                print(f"INTERSECTION: {ring[i]} & {ring[j]}: {intersection}")
                intersections.append(intersection)
                if ring[i].b == 0: #Is line vertical?
                    ring[i].limit = sorted([intersections[i-1].y,intersections[i].y])
                else:
                    ring[i].limit = sorted([intersections[i-1].x,intersections[i].x])
            if ring[0].b == 0:
                ring[0].limit = sorted([intersections[0].y, intersections[-1].y])
            else:
                ring[0].limit = sorted([intersections[0].x, intersections[-1].x])

        #generate
        checkpoints = []
        maximum_length = sum([abs(v) for v in directions])
        
        
        vertices = [item for sublist in paralel_lines for item in sublist]
        print(vertices)
        return (vertices, checkpoints)


        """
        Define bissectrice P
        If snijpunt(bissectrice P, L1) == snijpunt(bissectrice P, L2):
            limit updaten
        
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
                plines.append(line)
        """

        return plines


if __name__ == "__main__":
    # Testing
    window = pyglet.window.Window(resizable=True, fullscreen=True) 

    # inner_points = [[18,3],[8,3],[5,4],[3,6],[2,9],[2,12],[3,14],[4,14],[6,12],[7,8],[8,7],[12,6],[16,6],[19,9],[20,11],[16,13],[13,12],[12,14],[13,15],[17,16],[20,15],[22,13],[23,8],[21,5]]
    # inner = [Vector2D(i[0],i[1]) for i in inner_points]

    # outer_points = [[18,0],[8,0],[2,3],[0,9],[0,14],[2,16],[5,16],[8,12],[9,9],[12,8],[15,8],[17,10],[16,11],[12,10],[11,11],[10,13],[10,15],[12,17],[17,17],[20,16],[23,14],[25,8],[23,4]]
    # outer = [Vector2D(i[0],i[1]) for i in outer_points]


    # checkpoints = [[[10,-1],[10,4]],[[4,1],[6,4]],[[0,6],[3,7]],[[-1,13],[3,12]],[[4,13],[7,15]],[[6,9],[10,11]],[[11,5],[12,9]],[[15,10],[18,7]],[[15,10],[14,13]],[[9,14],[13,13]],[[15,17],[16,15]],[[21,12],[24,15]],[[22,8],[25,6]],[[19,5],[20,1]],[[15,-1],[15,4]]]
    # circuit_checkpoints = []
    # for i, checkpoint in enumerate(checkpoints):
    #     circuit_checkpoints.append([])
    #     for x, point in enumerate(checkpoint):
    #         circuit_checkpoints[i].append(Vector2D(point[0],point[1]))

    circ = circuit.fromSkeletonPoints([Vector2D(p[0],p[1]) for p in [[100,100],[100,400],[700,100]]])
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