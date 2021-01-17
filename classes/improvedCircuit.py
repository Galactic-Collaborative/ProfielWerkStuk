from __future__ import annotations

import pyglet
import json
import math
from classes.improvedLine import linline
from classes.Vector import Vector2D

from typing import List, Union

class circuit():
    def __init__(self, vertices: List[List[linline]], checkpoints: List[linline], skeletonLines: List[linline] = None, startingPoint=Vector2D(0,0), monocar: bool=True) -> None:
        self.innerLines = vertices[0]
        self.outerLines = vertices[1]
        self.vertices = [item for sublist in vertices for item in sublist]
        if checkpoints is None:
            self.checkpoints = self.generateCheckpoints(10)
        else:
            self.checkpoints = checkpoints

        self.currentCheckpoint = 0
        self.skeletonLines = skeletonLines


        self.startingPoint = startingPoint
        self.monocar = monocar
    
    @classmethod
    def fromSkeletonPoints(cls, points, startingPoint=Vector2D(0,0)):
        vertices, checkpoints, newStartingPoint = cls.generate(points, width=100, startingPoint=startingPoint)
        return cls(vertices, checkpoints, newStartingPoint)


    @classmethod
    def fromJSON(cls, filename, window=[1920,1080], method="Skeleton"):
        with open(filename, "r") as f:
            circuitDict = json.load(f)
        
        #Feature detection
        hasSkeleton = 'skeleton' in circuitDict.keys()
        hasCheckpoints = 'checkpoints' in circuitDict.keys()

        #Assign startingPoint to local variable
        startingPoint = Vector2D(circuitDict['startingPoint'][0], circuitDict['startingPoint'][1]) 

        #Convert lists of coordinates to Vector2D
        skeleton = [Vector2D(i[0],i[1]) for i in circuitDict['skeleton']] if hasSkeleton else None

        if hasSkeleton and method=="Skeleton":
            return cls.fromSkeletonPoints(skeleton, startingPoint=startingPoint)
        else:
            innerPoints = [Vector2D(i[0],i[1]) for i in circuitDict['inner']]
            outerPoints = [Vector2D(i[0],i[1]) for i in circuitDict['outer']]

            if hasCheckpoints: 
                checkpoints = [[Vector2D(i[0][0],i[0][1]), Vector2D(i[1][0], i[1][1])] for i in circuitDict['checkpoints']]
                return cls.fromFullPoints([innerPoints, outerPoints],
                        checkpoints=checkpoints, 
                        startingPoint=startingPoint,
                        window=window)
            else:
                return cls.fromFullPoints([innerPoints, outerPoints], 
                        startingPoint=startingPoint,
                        window=window)

    @classmethod
    def fromFullPoints(cls, 
            points: List[List[Vector2D]], 
            checkpoints: Union[List[List[Vector2D]],None] = None,
            skeletonPoints = None,
            numCheckpoints = 10, 
            startingPoint = Vector2D(0,0), 
            window = (1920,1080), 
            monocar: bool = True
        ) -> circuit:
        
        lines = []
        checkpoint = []
        margin = Vector2D(50,50)
        allpoints = [item for sublist in points for item in sublist]
        max_x = max([p.x for p in allpoints])
        max_y = max([p.y for p in allpoints])
        scale = min((window[0]-2*margin.x)/max_x, (window[1]-2*margin.y)/max_y)
        startPoint = startingPoint*scale + margin

        #Create a list of lines from the points
        for k, lane in enumerate(points):
            lines.append([])
            for i in range(len(lane)):
                j = (i+1)%len(lane)
                lines[k].append(linline.fromPoints(lane[i]*scale+margin,lane[j]*scale+margin))
        if checkpoints is not None:
            for line in checkpoints:
                l = linline.fromPoints(line[0]*scale+margin,line[1]*scale+margin)
                l.color = (255,215,0)
                checkpoint.append(l)
        
        skeletonLines = []
        if skeletonPoints is not None:
            for i in range(skeletonPoints):
                j = (i+1)%len(skeletonPoints)
                skeletonLines[i].append(linline.fromPoints(skeletonPoints[i]*scale+margin,skeletonPoints[j]*scale+margin))

        return cls(lines, checkpoint, startingPoint=startPoint, monocar=monocar, skeletonLines=skeletonLines)

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
        print(currentCheckpoint + 1)
        currentCheckpoint = (currentCheckpoint + 1)%len(self.checkpoints)
        return currentCheckpoint

    def draw(self, batch, screen, group):
        out = []
        for line in self.vertices:
            out.append(line.draw(batch, group, screen))
        


        if True:
            #out.append(self.checkpoints[self.currentCheckpoint - 1].draw(batch, group, screen))
            out.append(self.checkpoints[self.currentCheckpoint].draw(batch, group, screen))
            #out.append(self.checkpoints[(self.currentCheckpoint + 1)%len(self.checkpoints)].draw(batch, group, screen))
        else:
            for i, line in enumerate(self.checkpoints):
                out.append(line.draw(batch, group, screen))

        return out
    
    @staticmethod
    def generate(points: list, width:int=100, numCheckpoints=10, startingPoint=Vector2D(0,0), window=[1920,1080]) -> List[linline]:
        r = width/2
        
        lines = []
        directions = []

        #generate scale and apply
        margin = Vector2D(50,50)
        max_x = max([p.x for p in points])
        max_y = max([p.y for p in points])
        scale = min((window[0]-2*margin.x)/max_x, (window[1]-2*margin.y)/max_y)
        scaledStartingPoint = startingPoint*scale + margin

        points[:] = [point*scale + margin for point in points]

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
                c = lines[i].n @ w
                paralel_lines[j].append(linline(lines[i].a, lines[i].b, c))


        print(len(paralel_lines))
        #Generate joint points
        for ring in paralel_lines:
            intersections = []
            intersections.append(ring[0].intersect(ring[1]))
            for i in range(1,len(ring)):
                j = (i+1)%len(ring)
                intersection = ring[i].intersect(ring[j])
                intersections.append(intersection)
                if ring[i].b == 0: #Is line vertical?
                    ring[i].limit = [intersections[i-1].y,intersections[i].y]
                else:
                    ring[i].limit = [intersections[i-1].x,intersections[i].x]
            if ring[0].b == 0:
                ring[0].limit = [intersections[0].y, intersections[-1].y]
            else:
                ring[0].limit = [intersections[0].x, intersections[-1].x]

        #generate
        checkpoints = [linline(1,0,0)] # circuit.generateCheckpoints(paralel_lines, numCheckpoints=numCheckpoints)
        maximum_length = sum([abs(v) for v in directions])

        return (paralel_lines, scaledStartingPoint)
    
    def generateCheckpoints(self, numCheckpoints=10):
        self.numCheckpoints = numCheckpoints
        print(numCheckpoints)
        color = (
            (255,0,0),
            (0,255,0),
            (0,0,255),
            (255,255,0),
            (255,0,255),
            (0,255,255),
        )
        checkpoints = [[],[]]

        def appendToCheckpoint(lengthUntilNextCheckpoint, checkpoints, line, currentLengthOfLine, ratioOfLengthToNextCheckpoint):
            beginOfCurrentLine, _ = line.getEndPoints()
            newCheckpoint = beginOfCurrentLine + line.r.normalize(in_place=False) * ratioOfLengthToNextCheckpoint
            checkpoints[0].append(newCheckpoint)

            perpindicular = linline.fromVector(line.n, newCheckpoint)
            distance = math.inf
            secondNewCheckpoint = Vector2D(0,0)
            for outerLine in self.innerLines:
                intersection = perpindicular.intersect(outerLine)
                if intersection is not None:
                    if abs(newCheckpoint - intersection) < distance:
                        distance = abs(newCheckpoint - intersection)
                        secondNewCheckpoint = intersection

            checkpoints[1].append(secondNewCheckpoint)

        lengthOfLine = []
        for line in self.outerLines:
            pointA, pointB = line.getEndPoints()
            lengthOfLine.append(abs(pointA - pointB))
        
        fullLength = sum(lengthOfLine)
        gapBetweenCheckpoints = fullLength / numCheckpoints
        currentLengthOfLine = lengthOfLine

        untilNextCheckpoint = gapBetweenCheckpoints

        for j, line in enumerate(self.outerLines):
            if(untilNextCheckpoint - currentLengthOfLine[j] > 0):
                print("NEXT")
                untilNextCheckpoint -= currentLengthOfLine[j]
            else:
                ratioOfLengthToNextCheckpoint = untilNextCheckpoint / currentLengthOfLine[j]
                print(ratioOfLengthToNextCheckpoint)
                appendToCheckpoint(untilNextCheckpoint, checkpoints, line, currentLengthOfLine[j], ratioOfLengthToNextCheckpoint)
                
                while(gapBetweenCheckpoints - (1-ratioOfLengthToNextCheckpoint) * currentLengthOfLine[j] < 0):
                    print("I AM THE CULPRIT")
                    untilNextCheckpoint = gapBetweenCheckpoints + untilNextCheckpoint
                    ratioOfLengthToNextCheckpoint = (untilNextCheckpoint) / currentLengthOfLine[j]
                    appendToCheckpoint(untilNextCheckpoint, checkpoints, line, currentLengthOfLine[j], ratioOfLengthToNextCheckpoint)
                
                untilNextCheckpoint = gapBetweenCheckpoints - (1-ratioOfLengthToNextCheckpoint) * currentLengthOfLine[j]
        
        checkpointLines = []
        for i in range(len(checkpoints[0])):
            print(checkpoints[1][i])
            line = linline.fromPoints(checkpoints[0][i],checkpoints[1][i])
            line.color = color[i%len(color)]
            checkpointLines.append(line)
        
        return checkpointLines

    # def generateVisualCheckpoints(self, batch, group):
    #     checkpoints = [[],[]]
    #     colors = [
    #         (255,0,0),
    #         (0,255,0),
    #         (0,0,255)
    #     ]
    #     lengthOfLine = []
    #     for i, line in enumerate(self.outerLines):
    #         pointA, pointB = line.getEndPoints()
    #         lengthOfLine.append(abs(pointA - pointB))
        
    #     fullLength = sum(lengthOfLine)
        
    #     gapBetweenCheckpoints = fullLength / self.numCheckpoints
    #     currentLengthOfLine = lengthOfLine
    #     checkpointsLines2 = []
    #     untilNextCheckpoint = gapBetweenCheckpoints
    #     for j, line in enumerate(self.outerLines):
    #         if(untilNextCheckpoint - currentLengthOfLine[j] > 0):
    #             untilNextCheckpoint -= currentLengthOfLine[j]
    #         else:
    #             beginOfCurrentLine, _ = line.getEndPoints()
    #             ratioOfLengthToNextCheckpoint = untilNextCheckpoint / currentLengthOfLine[j]
                
    #             newCheckpoint = beginOfCurrentLine + -line.r * ratioOfLengthToNextCheckpoint
    #             checkpoints[0].append(newCheckpoint)

    #             perpindicular = linline.fromVector(line.n, newCheckpoint)
    #             checkpointsLines2.append(perpindicular.draw(batch, group, screen=[2560,1440]))
    #             distance = math.inf
    #             secondNewCheckpoint = Vector2D(0,0)
    #             for outerLine in self.innerLines:
    #                 intersection = perpindicular.intersect(outerLine)
    #                 if intersection is not None:
    #                     if abs(newCheckpoint - intersection) < distance:
    #                         distance = abs(newCheckpoint - intersection)
    #                         secondNewCheckpoint = intersection

    #             checkpoints[1].append(secondNewCheckpoint)
                
    #             untilNextCheckpoint = gapBetweenCheckpoints - (1 - ratioOfLengthToNextCheckpoint)*currentLengthOfLine[j]
        
    #     checkpointLines = []
    #     for i in range(len(checkpoints[0])):
    #         checkpointLines.append(pyglet.shapes.Circle(checkpoints[0][i].x, checkpoints[0][i].y, 10, color=colors[i%3], batch=batch, group=group))
    #         checkpointLines.append(pyglet.shapes.Circle(checkpoints[1][i].x, checkpoints[1][i].y, 10, batch=batch, group=group))
        
    #     return checkpointLines, checkpointsLines2






    def reset(self):
        self.currentCheckpoint = 0;


if __name__ == "__main__":
    circuit.fromJSON("../circuits/BONK_CIRCUIT.json")