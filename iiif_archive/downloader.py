import requests
import json
import os
import zipfile
import logging
import time
from .processors import manifest_factory, infoJson_factory

from iiif_archive.config import get_config

logger = logging.getLogger(__name__)

def zip(source_dir, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=source_dir)
                zipf.write(file_path, arcname)

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

def downloadAsset(filename, url, retries=3):
    config = get_config()
    if os.path.exists(filename):
        logger.info(f"Found {url} already present in {filename}.")
    else:
        for attempt in range(1, retries + 1):
            try:
                with requests.get(url, stream=True) as response:
                    response.raise_for_status()  # Raises error for bad status
                    with open(filename, "wb") as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:  # filter out keep-alive chunks
                                f.write(chunk)

                time.sleep(config.delay)                

                return filename
            except requests.exceptions.HTTPError as e:
                if response.status_code == 502:
                    logger.info(f"Attempt {attempt} failed with 502 Bad Gateway.")
                    if attempt < retries:
                        time.sleep(config.retry_delay)
                        continue
                raise e # Re-raise if not 502 or retries exhausted

    return filename

def downloadIIIF(imageDir, url):
    os.makedirs(imageDir, exist_ok=True)
    # Download info.json
    infoJson = infoJson_factory(saveJson(f"{url}/info.json", os.path.join(imageDir, "info.json")))

    urls = infoJson.tileUrls()
    for url in urls:
        filename = url.replace(infoJson.id, imageDir)
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        try:
            downloadAsset(filename, url)
        except requests.exceptions.HTTPError as e:    
            print(f"Failed to get {url} skipping.")

def download(url, zipFileName, scratch="downloads", deleteScratch=True):
    """Downloads and processes a IIIF manifest from the given URL and stores the result in a zip file.

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
        logger.info(f"Downloading {container.url}")
        if container.isDownloadable():
            downloadAsset(os.path.join(downloadDir, container.filename), container.url)

            container.url = container.filename
        else:
            # Content is a IIIF Image 
            downloadIIIF(os.path.join(downloadDir, container.filename), container.url)    

            container.url = container.filename

    manifest.save(os.path.join(downloadDir, "manifest.json"))        

    zip(downloadDir, zipFileName)

    return zipFileName