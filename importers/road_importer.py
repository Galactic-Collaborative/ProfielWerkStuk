import math
from mathematics.lines import Line, BoundedLine
from mathematics.vector import Vector2D
from road import Road
from typing import Any


def import_json(data: Any) -> Road:
    """Import a circuit from a JSON file

    Args:
        fileName (str): The file name of the JSON file

    Returns:
        Circuit: The imported circuit
    """
    type : str = data["road"]["generator"]
    match type:
        case "skeleton":
            return import_skeleton(data["road"])
        case "custom":
            return import_custom(data["road"])
        case _:
            raise ValueError(f"Unknown road type: {type}")


def import_skeleton(data: Any) -> Road:
    """Import a skeleton road from a JSON file

    The road must have a inner and outer line defined

    Args:
        data (JSON): The data of the road

    Returns:
        Road: The imported Road
    """

    skeleton = [Vector2D(point[0], point[1]) for point in data["points"]]
    width = float(data["width"])

    (inner, outer) = create_road_from_skeleton(skeleton, width)

    return Road(inner, outer)


def import_custom(data : Any) -> Road:
    """Import a custom road from a JSON file

    The road must have a inner and outer line defined

    Args:
        data (JSON): The data of the road

    Returns:
        Road: The imported Road
    """

    outer = create_lines_from_data(data["outer"])
    inner = create_lines_from_data(data["inner"])

    return Road(outer, inner)


def create_lines_from_data(points : list[list[float]]) -> list[BoundedLine]:
    """Create a line from a list of points

    Args:
        points (list[Real]): The points of the line

    Returns:
        Line: The created line
    """

    vector_points = [Vector2D(point[0], point[1]) for point in points]

    return create_lines(vector_points)


def create_lines(points: list[Vector2D]) -> list[BoundedLine]:
    """Create a line from a list of points

    Args:
points (list[Vector2D]): The points of the line

    Returns:
        Line: The created line
    """

    lines : list[BoundedLine] = []

    previous_point = points[0]
    for point in points[1:]:
        lines.append(BoundedLine.from_points(previous_point, point))
        previous_point = point

    lines.append(BoundedLine.from_points(previous_point, points[0]))

    return lines


def create_road_from_skeleton(skeleton : list[Vector2D], width: float) -> tuple[list[BoundedLine], list[BoundedLine]]:
    """Create a road from a skeleton

    Args:
        skeleton (list[Line]): The skeleton of the road
        width (float): The width of the road

    Returns:
        tuple[list[Line], list[Line]]: The inner and outer lines of the road
    """

    inner_points : list[Vector2D] = []
    outer_points : list[Vector2D] = []

    previousPoint = skeleton[-2]
    currentPoint = skeleton[-1]
    for nextPoint in skeleton:
        r = (currentPoint - previousPoint).normalized()
        l = (currentPoint - nextPoint).normalized()

        d = (r + l).normalized()

        if(r.rotate(math.pi/2) @ l >= 0):
            inner_points.append(currentPoint + d * width / 2)
            outer_points.append(currentPoint - d * width / 2)
        else:
            inner_points.append(currentPoint - d * width / 2)
            outer_points.append(currentPoint + d * width / 2)

        previousPoint = currentPoint
        currentPoint = nextPoint

    inner = create_lines(inner_points)
    outer = create_lines(outer_points)

    return (inner, outer)