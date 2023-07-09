from __future__ import annotations
import json
from mathematics.lines import BoundedLine
from mathematics.vector import Vector2D
from typing import TYPE_CHECKING
from circuit import Circuit

if TYPE_CHECKING:
    from typing import Any


def load_json(data: Any) -> Circuit:
    """Load a circuit from a JSON file

    Args:
        data (JSON): The data of the circuit

    Returns:
        Circuit: The loaded circuit
    """
    from importers.road_importer import import_json as import_road

    road = import_road(data)

    starting_point: Vector2D = Vector2D(data["starting_point"][0], data["starting_point"][1])
    checkpoints: list[BoundedLine] = create_checkpoint_lines(data["checkpoints"])

    return Circuit(road, starting_point, checkpoints)


def create_checkpoint_lines(checkpoints: list[list[list[float]]]) -> list[BoundedLine]:
    """Create checkpoint lines from a list of floats

    Args:
        checkpoints (list[list[list[float]]]): The checkpoints

    Returns:
        list[Line]: The checkpoint lines
    """
    lines: list[BoundedLine] = []

    for checkpoint in checkpoints:
        lines.append(BoundedLine.from_points(Vector2D(checkpoint[0][0], checkpoint[0][1]), Vector2D(checkpoint[1][0], checkpoint[1][1])))

    return lines