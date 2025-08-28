import argparse
import logging

from iiif_archive import downloader
from iiif_archive.config import Config, load_config

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    default = Config()

    parser = argparse.ArgumentParser(description="Download a Manifest and store the results in a zip file")
    parser.add_argument("manifest", help="https URL to the manifest")
    parser.add_argument("--zip-file-name", type=str, default="downloads/manifest.zip", help="Name of the zip file (default: manifest.zip)")
    parser.add_argument("--conf", type=str, default="conf/config.ini", help="Config file. Default: conf/config.ini")
    parser.add_argument("--delay", type=str, help=f"Delay between image requests in seconds. Use 0 for no delay. Default: {default.delay} second.")
    parser.add_argument("--retry-delay", type=str, help=f"Delay between image requests after getting a 503 from the first attempt (in seconds). Use 0 for no delay. Default: {default.retry_delay} second.")

    args = parser.parse_args()

    params = {}
    if args.delay:
        params["delay"] = args.delay

    if args.retry_delay:
        params["retry_delay"] = args.retry_delay

    print(params)

    config = load_config(args.conf, params)

    filename = downloader.download(args.manifest, args.zip_file_name, config.scratch_dir)

    print(f"Created {filename}")
