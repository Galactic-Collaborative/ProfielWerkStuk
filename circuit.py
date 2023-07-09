import json
from mathematics.vector import Vector2D
from mathematics.lines import BoundedLine
from road import Road


class Circuit:
    """A circuit is a road with a start line and checkpoints
    """

    road: Road
    starting_point: Vector2D
    checkpoints: list[BoundedLine]

    def __init__(self, road: Road, starting_point: Vector2D, checkpoints: list[BoundedLine]):
        """Create a new circuit

        Args:
            road (Road): The road of the circuit
            starting_point (Vector2D): The starting point of the circuit
            checkpoints (list[Line]): The checkpoints of the circuit
        """
        self.road = road
        self.starting_point = starting_point
        self.checkpoints = checkpoints

    @classmethod
    def from_json(cls, filename: str):
        """Create a new circuit from a JSON file

        Args:
            filename (str): The file name of the JSON file

        Returns:
            Circuit: The created circuit
        """
        with open(filename, "r") as f:
            data = json.load(f)

        from importers.circuit_importer import load_json as import_circuit
        return import_circuit(data)
