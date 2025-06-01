from iiif_archive import downloader
import logging
import argparse

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="Download a Manifest and store the results in a zip file")
    parser.add_argument("manifest", help="https URL to the manifest")
    parser.add_argument("--zip-file-name", type=str, default="downloads/manifest.zip", help="Name of the zip file (default: manifest.zip)")
    parser.add_argument("--conf", type=str, default="conf/config.ini", help="Config file")

    args = parser.parse_args()
    #Config.load(args.conf)
    filename = downloader.download(args.manifest, args.zip_file_name)

    print (f"Created {filename}")