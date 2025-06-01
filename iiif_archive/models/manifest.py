from abc import ABC, abstractmethod
from typing import Dict, Any
import json

from iiif_archive.models.container import Canvas3, Canvas2

class Manifest(ABC):
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    @abstractmethod
    def containers(self):
        pass

    def save(self, filename):
        with open(filename, "w") as f:
            json.dump(self.data, f, indent=4)

        return self.data

class Manifest2(Manifest):
    def containers(self):
        canvases = []
        for sequence in self.data["sequences"]:    
            for canvas in sequence["canvases"]:
                canvases.append(Canvas2(canvas))

        return  canvases

class Manifest3(Manifest):
    def containers(self):
        canvases = []
        for canvas in self.data["items"]: 
            canvases.append(Canvas3(canvas))
        return canvases

