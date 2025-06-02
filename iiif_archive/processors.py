from typing import Dict, Any

from iiif_archive.models.manifest import Manifest, Manifest2, Manifest3
from iiif_archive.models.container import Container, Canvas2, Canvas3
from iiif_archive.models.infoJson import InfoJson, InfoJson2, InfoJson3

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
        raise ValueError(f"Unknown manifest version: {manifest['@context']}")


def container_factory(container: Dict[str, Any]) -> Container:    
    if "@type" in container:
        return Canvas2(container)
    else:
        return Canvas3(container)    

def infoJson_factory(data: Dict[str, Any]) -> InfoJson:
    contexts = data["@context"]
    # Ensure contexts is an array for consistency 
    if isinstance(contexts, str):
        contexts = [contexts]

    if "http://iiif.io/api/image/3/context.json" in contexts:
        return InfoJson3(data)
    elif "http://iiif.io/api/image/2/context.json" in contexts:
        return InfoJson2(data)
    else:
        raise ValueError(f"Unknown info.json version: {data['@context']}")
