from iiif_archive import decompressor
import logging
import argparse

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="Export a zipped Manifest so it can be served at a specified URL")
    parser.add_argument("zip_file", help="zip_file to inflate")
    parser.add_argument("local_dir", help="directory to inflate zip file to")
    parser.add_argument("base_url", help="base URL that the manifest will be served at")

    args = parser.parse_args()
    dir = decompressor.inflate(args.zip_file, args.local_dir, args.base_url)

    print (f"Inflated to: {dir}")