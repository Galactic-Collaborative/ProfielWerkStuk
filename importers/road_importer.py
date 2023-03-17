from mathematics.lines import Line
from mathematics.vector import Vector2D
from road import Road
from typing import Any


def ImportJSON(data: Any) -> Road:
    """Import a circuit from a JSON file

    Args:
        fileName (str): The file name of the JSON file

    Returns:
        Circuit: The imported circuit
    """
    type : str = data["road"]["generator"]
    match type:
        case "skeleton":
            return ImportSkeleton(data["road"])
        case "custom":
            return ImportCustom(data["road"])
        case _:
            raise ValueError(f"Unknown road type: {type}")


def ImportSkeleton(data: Any) -> Road:
    """Import a skeleton road from a JSON file

    The road must have a inner and outer line defined

    Args:
        data (JSON): The data of the road

    Returns:
        Road: The imported Road
    """

    skeleton = [Vector2D(point[0], point[1]) for point in data]
    width = data["width"]

    (inner, outer) = createRoadFromSkeleton(skeleton, width)

    return Road(inner, outer)

def ImportCustom(data : Any) -> Road:
    """Import a custom road from a JSON file

    The road must have a inner and outer line defined

    Args:
        data (JSON): The data of the road

    Returns:
        Road: The imported Road
    """

    outer = CreateLinesFromData(data["outer"])
    inner = CreateLinesFromData(data["inner"])

    return Road(outer, inner)

def CreateLinesFromData(points : list[list[float]]) -> list[Line]:
    """Create a line from a list of points

    Args:
        points (list[Real]): The points of the line

    Returns:
        Line: The created line
    """

    vectorPoints = [Vector2D(point[0], point[1]) for point in points]

    return CreateLines(vectorPoints)

def CreateLines(points: list[Vector2D]) -> list[Line]:
    """Create a line from a list of points

    Args:
points (list[Vector2D]): The points of the line

    Returns:
        Line: The created line
    """

    lines : list[Line] = []

    prevPoint = points[0]
    for point in points[1:]:
        lines.append(Line(prevPoint, point))
        prevPoint = point

    lines.append(Line(prevPoint, points[0]))

    return lines

def createRoadFromSkeleton(skeleton : list[Vector2D], width: float) -> tuple[list[Line], list[Line]]:
    """Create a road from a skeleton

    Args:
        skeleton (list[Line]): The skeleton of the road
        width (float): The width of the road

    Returns:
        tuple[list[Line], list[Line]]: The inner and outer lines of the road
    """

    innerPoints : list[Vector2D] = []
    outerPoints : list[Vector2D] = []

    a = skeleton[0]
    b = skeleton[1]
    for c in skeleton[2:]:
        r = (b - a).Normalize()
        l = (b - c).Normalize()

        d = (r + l).Normalize()

        innerPoints.append(b + d * width / 2)
        outerPoints.append(b - d * width / 2)

        a = b
        b = c

    inner = CreateLines(innerPoints)
    outer = CreateLines(outerPoints)

    return (inner, outer)