from abc import ABC, abstractmethod
from typing import Dict, Any
import math

class InfoJson(ABC):
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    @property
    def width(self) -> int:
        return self.data["width"]    

    @property
    def height(self) -> int:
        return self.data["height"]    

    @property    
    @abstractmethod
    def id(self) -> str:
        pass

    def tileUrls(self):
        tiles = self.data["tiles"][0]
        tileWidth = tiles["width"]
        tileHeight = tiles["height"]

        urls = []
        # structure is the same for both versions
        for scaleFactor in tiles["scaleFactors"]:
            urls += self.scaleTiles(scaleFactor, tileWidth, tileHeight)

        return urls    

    def scaleTiles(self, scaleFactor, tileWidth, tileHeight):
        urls = []
        scaledWidth = math.ceil(self.width / scaleFactor)
        scaledHeight = math.ceil(self.height / scaleFactor)
        # Work out if resulting image is smaller than the tileWidth
        if scaledWidth <= tileWidth:
            # ask for the full size
            urls.append(self.buildImage(sizeWidth=scaledWidth, sizeHeight=scaledHeight))
        else:
            scaledTileWidth = scaleFactor * tileWidth
            scaledTileHeight = scaleFactor * tileHeight

            tilesWide = math.ceil(self.width / scaledTileWidth)
            tilesHigh = math.ceil(self.height / scaledTileHeight)

            for x in range(0, tilesWide):
                for y in range(0, tilesHigh):
                    left = x * scaledTileWidth
                    width = scaledTileWidth
                    if left + width > self.width:
                        width = self.width - left

                    top = y * scaledTileHeight    
                    height = scaledTileHeight
                    if top + height > self.height:
                        height = self.height - top

                    region = f"{left},{top},{width},{height}"
                    urls.append(self.buildImage(region=region, sizeWidth=math.ceil(width / scaleFactor), sizeHeight=math.ceil(height / scaleFactor)))

        return urls    

    @abstractmethod
    def buildImage(self, region="full", sizeWidth=0, sizeHeight=0, rotation=0, quality="default", format="jpg"):
        pass

class InfoJson2(InfoJson):    
    @property
    def id(self):
        return self.data['@id']

    def buildImage(self, region="full", sizeWidth=0, sizeHeight=0, rotation=0, quality="default", format="jpg"):
        return f"{self.data['@id']}/{region}/{sizeWidth},/{rotation}/{quality}.{format}"

class InfoJson3(InfoJson):    
    @property
    def id(self):
        return self.data['id']

    def buildImage(self, region="full", sizeWidth=0, sizeHeight=0, rotation=0, quality="default", format="jpg"):
        return f"{self.data['id']}/{region}/{sizeWidth},{sizeHeight}/{rotation}/{quality}.{format}"
    
