from abc import ABC, abstractmethod
from typing import Dict, Any
import os
import json

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

def manifest_factory(manifest: Dict[str, Any]) -> Manifest:
    contexts = manifest["@context"]
    # Ensure contexts is an array for consistency 
    if isinstance(contexts, str):
        contexts = [contexts]

    if "http://iiif.io/api/presentation/2/context.json" in contexts:
        return Manifest2(manifest)
    elif "http://iiif.io/api/presentation/3/context.json" in contexts:
        return Manifest3(manifest)
    else:
        raise ValueError(f"Unknown manifest version: {manifest["@context"]}")

class Container(ABC):
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    @property
    @abstractmethod
    def id(self) -> str:
        """Abstract property that must be implemented."""
        pass    

    @property
    @abstractmethod
    def url(self) -> str:
        """The URL of the asset or IIIF image Id"""
        pass

    @url.setter
    @abstractmethod
    def url(self, value) -> str:
        """Set the URL of the asset or IIIF image Id"""
        pass

    @property
    @abstractmethod
    def filename(self) -> str:
        pass

    @abstractmethod
    def isDownloadable(self) -> bool:
        pass


class Canvas2(Container):    
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    @property
    def id(self):
        return self.data["@id"]

    @property
    def url(self) -> str:
        if self.isDownloadable():
            return self.data["images"][0]["resource"]["@id"]
        else: 
            return self.data["images"][0]["resource"]["service"]["@id"]

    @url.setter
    def url(self, value) -> str:
        if self.isDownloadable():
            self.data["images"][0]["resource"]["@id"] = value
        else: 
            self.data["images"][0]["resource"]["service"]["@id"] = value

    @property
    def filename(self) -> str:
        return os.path.basename(self.url)

    def isDownloadable(self) -> bool:
        if len(self.data["images"]) > 1:
            raise NotImplementedError("iiif-archive doesn't support composite images")

        imageResource = self.data["images"][0]["resource"]
            
        return "service" not in imageResource    


class Canvas3(Container):    
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    @property
    def id(self):
        return self.data["id"]

    @property
    def url(self) -> str:
        if self.isDownloadable():
            return self.data["items"][0]["items"][0]["body"]["id"]
        else: 
            service = self.data["items"][0]["items"][0]["body"]["service"]
            imgId = ""
            if "@id" in service:
                # In case v3 manifest is linking to a v2 image
                imgId = service["@id"]
            else:
                imgId = service["id"]

            return imgId

    @url.setter
    def url(self, value) -> str:
        if self.isDownloadable():
            self.data["items"][0]["items"][0]["body"]["id"] = value
        else: 
            service = self.data["items"][0]["body"]["service"]
            if "@id" in service:
                # In case v3 manifest is linking to a v2 image
                service["@id"] = value
            else:
                service["id"] = value


    def isDownloadable(self) -> bool:
        if len(self.data["items"]) > 1:
            raise NotImplementedError("iiif-archive doesn't support multiple annotation pages")

        if len(self.data["items"][0]["items"]) > 1:
            raise NotImplementedError("iiif-archive doesn't support composite images")

        imageResource = self.data["items"][0]["items"][0]["body"]
            
        return "service" not in imageResource 

    @property
    def filename(self) -> str:
        return os.path.basename(self.url)
        

def container_factory(container: Dict[str, Any]) -> Container:    
    if "@type" in container:
        return Canvas2(container)
    else:
        return Canvas3(container)    
