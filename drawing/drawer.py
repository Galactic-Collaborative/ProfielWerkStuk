import pyglet
from pyglet.canvas.base import Screen
from pyglet.graphics import Batch, Group
from dataclasses import dataclass
import abc
from pyglet.window import Window
from mathematics.lines import BoundedLine, Line, Ray
from mathematics.vector import Vector2D

Shape = pyglet.shapes.ShapeBase
DrawingReference = list[Shape]


@dataclass
class RenderOptions:
    detailsOnly: bool = False


class DrawingInterface(abc.ABC):
    @abc.abstractmethod
    def draw(self, batch: Batch, window: Window, group: Group, options: RenderOptions) -> DrawingReference:
        """Draw the object to the screen

        Args:
            batch (Batch): The pyglet render batch
            screen (Screen): The screen to draw to
            group (Group): The group to draw in
            options (RenderOptions): The optional render options
        """
        pass


def drawLine(line: Line, batch: Batch, window: Window, group: Group) -> Shape:
    """Draw a line to the screen

    Args:
        line (Line): The line to draw
        batch (Batch): The pyglet render batch
        screen (Screen): The screen to draw to
        group (Group): The group to draw in
    """

    # Define the screen
    top: BoundedLine = BoundedLine.from_points(Vector2D(0,window.height), Vector2D(window.width,window.height))
    bottom: BoundedLine = BoundedLine.from_points(Vector2D(0,0), Vector2D(window.width,0))
    left: BoundedLine = BoundedLine.from_points(Vector2D(0,0), Vector2D(0,window.height))
    right: BoundedLine = BoundedLine.from_points(Vector2D(window.width,0), Vector2D(window.width,window.height))


    # Search the boundaries of the line on the screen
    min_vec = Vector2D(0,0)
    max_vec = Vector2D(0,0)

    positive_ray = Ray(line.origin, line.direction);
    negative_ray = Ray(line.origin, -line.direction);

    for boundary in [top, bottom, left, right]:
        if (intersection := boundary.intersect(positive_ray)):
            max_vec = intersection

        if (intersection := boundary.intersect(negative_ray)):
            min_vec = intersection

    # Draw the line
    return pyglet.shapes.Line(
        min_vec.x, min_vec.y, max_vec.x, max_vec.y, batch=batch, group=group
    )

def drawBoundedLine(line: BoundedLine, batch: Batch, screen: Screen, group: Group) -> Shape:
    """Draw a line to the screen

    Args:
        line (Line): The line to draw
        batch (Batch): The pyglet render batch
        screen (Screen): The screen to draw to
        group (Group): The group to draw in
    """

    end = line.calc(line.length)

    return pyglet.shapes.Line(
            line.origin.x, line.origin.y, end.x, end.y, batch=batch, group=group
        )