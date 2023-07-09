from __future__ import annotations
from pyglet.graphics import Batch, Group
from circuit import Circuit
from .drawer import DrawingInterface, DrawingReference, RenderOptions, drawLine, drawBoundedLine
from road import Road
from pyglet.window import Window


class CircuitDrawer(DrawingInterface):
    circuit: Circuit
    road_drawer: RoadDrawer

    def __init__(self, circuit: Circuit):
        self.circuit = circuit
        self.road_drawer = RoadDrawer(circuit.road)

    def draw(
        self, batch: Batch, window: Window, group: Group, options: RenderOptions
    ):
        drawReferences: DrawingReference = []

        if not options.detailsOnly:
            drawReferences += (self.road_drawer.draw(batch, window, group, options))

        return drawReferences


class RoadDrawer(DrawingInterface):
    road: Road

    def __init__(self, road: Road):
        self.road = road

    def draw(
        self, batch: Batch, window: Window, group: Group, options: RenderOptions
    ) -> DrawingReference:
        drawReferences: DrawingReference = []

        for line in self.road.whole:
            drawReferences.append(drawBoundedLine(line, batch, window, group))

        return drawReferences