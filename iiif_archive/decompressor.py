import zipfile
import os
import json
from pathlib import Path

from iiif_archive.processors import manifest_factory, infoJson_factory

def unzip_file(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)


def inflate(zip_file, local_dir, base_url):
    unzip_file(zip_file, os.path.join(local_dir, zip_file.replace(".zip", "")))
    baseDir = os.path.join(local_dir, zip_file.replace(".zip", ""))

    base_url = base_url + "/" + zip_file.replace(".zip", "")

    with open(os.path.join(baseDir,"manifest.json"), "r") as f:
        manifest = manifest_factory(json.load(f))

        manifest.id = f"{base_url}/manifest.json"

        for container in manifest.containers():
            container.url = f"{base_url}/{container.url}"

        manifest.save(os.path.join(baseDir, "manifest.json"))

    baseDirPath = Path(baseDir)

    for subdir in baseDirPath.iterdir():
        if subdir.is_dir():
            with open(os.path.join(baseDir, subdir ,"info.json"), "r") as f:
                infoJson = infoJson_factory(json.load(f))

                infoJson.id = f"{base_url}/{os.path.basename(subdir)}"

                infoJson.save(os.path.join(baseDir, subdir ,"info.json"))
            
    return baseDir
