
import argparse
import requests
import json
import os
# from config import Config
import logging
from .processors import manifest_factory, Manifest

logger = logging.getLogger(__name__)

def saveJson(url, filename):
    # File already exists so return it
    if os.path.exists(filename):
        logger.info(f"Found {filename} already downloaded so returning that.")
        with open(filename, "r") as f:
            data = json.load(f)
            return data
    else:
        # Download manifest
        response = requests.get(url)

        # Raise an error for bad responses
        response.raise_for_status() 

        # Parse JSON
        data = response.json()
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

        return data    

def downloadAsset(filename, url):
    if os.path.exists(filename):
        logger.info(f"Found {url} already present in {filename}.")
    else:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()  # Raises error for bad status
            with open(filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # filter out keep-alive chunks
                        f.write(chunk)

    return filename

def download(url, zipFileName, scratch="downloads", deleteScratch=True):
    """
    Downloads and processes a IIIF manifest from the given URL and stores the result in a zip file.

    Args:
        url (str): The URL of the IIIF manifest to download.
        zipFileName (str): The name of the output zip file (e.g., "output.zip").
        scratch (str, optional): Directory to store temporary files. Defaults to "downloads".
        deleteScratch (bool, optional): Whether to delete the scratch directory after completion. Defaults to True.

    Returns:
        None

    Raises:
        requests.HTTPError: If the download fails.
        OSError: If writing to disk fails.
        ValueError: If the manifest is invalid or not supported.
    """

    if zipFileName.endswith(".zip"):
        dirname = os.path.basename(zipFileName).replace(".zip", "")
    else:
        dirname = os.path.basename(zipFileName)
        zipFileName += ".zip"    

    # Config.get("locations", "scratch_dir")
    downloadDir = os.path.join(scratch, dirname)

    os.makedirs(downloadDir, exist_ok=True)

    logger.info(f"Downloading {url}")
    manifest_json = saveJson(url, os.path.join(downloadDir, "manifest.json"))
    manifest = manifest_factory(manifest_json)


    for container in manifest.containers():
        if container.isDownloadable():
            filename = downloadAsset(os.path.join(downloadDir, container.filename), container.url)

            container.url = container.filename

    manifest.save(os.path.join(downloadDir, "manifest.json"))        

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="Download a Manifest and store the results in a zip file")
    parser.add_argument("manifest", help="https URL to the manifest")
    parser.add_argument("--zip-file-name", type=str, default="downloads/manifest.zip", help="Name of the zip file (default: manifest.zip)")
    parser.add_argument("--conf", type=str, default="conf/config.ini", help="Config file")

    args = parser.parse_args()
    #Config.load(args.conf)
    download(args.manifest, args.zip_file_name)