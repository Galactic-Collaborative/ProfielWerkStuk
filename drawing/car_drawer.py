from __future__ import annotations
from pyglet.canvas.base import Screen
from pyglet.graphics import Batch, Group
from car import Car
from .drawer import DrawingInterface, DrawingReference, RenderOptions, drawLine, drawBoundedLine
from pyglet.window import Window


class CarDrawer(DrawingInterface):
    car: Car

    def __init__(self, circuit: Car):
        self.circuit = circuit

    def draw(
        self, batch: Batch, window: Window, group: Group, options: RenderOptions
    ):
        drawReferences: DrawingReference = []

        corner_points = self.car.shape

        if not options.detailsOnly:
            drawReferences += (self.road_drawer.draw(batch, window, group, options))

        return drawReferences
