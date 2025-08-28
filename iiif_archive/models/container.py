import os
from abc import ABC, abstractmethod
from typing import Any, Dict


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
        """The URL of the asset or IIIF image Id."""
        pass

    @url.setter
    @abstractmethod
    def url(self, value) -> str:
        """Set the URL of the asset or IIIF image Id."""
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
            service = self.data["items"][0]["items"][0]["body"]["service"][0]
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
            service = self.data["items"][0]["items"][0]["body"]["service"][0]
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
