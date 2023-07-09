from abc import ABC, abstractmethod
import numpy as np
from mathematics.lines import Ray

class Shape(ABC):
    @abstractmethod
    def intersect(self, ray: Ray) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_mesh(self, resolution: int | None = None) -> np.ndarray:
        raise NotImplementedError