from iiif_archive import downloader, config
from iiif_archive.config import Config, get_config, load_config
import logging
import argparse

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    config = Config()

    parser = argparse.ArgumentParser(description="Download a Manifest and store the results in a zip file")
    parser.add_argument("manifest", help="https URL to the manifest")
    parser.add_argument("--zip-file-name", type=str, default="downloads/manifest.zip", help="Name of the zip file (default: manifest.zip)")
    parser.add_argument("--conf", type=str, default="conf/config.ini", help=f"Config file. Default: conf/config.ini")
    parser.add_argument("--delay", type=str, help=f"Delay between image requests in seconds. Use 0 for no delay. Default: {config.delay} second.")
    parser.add_argument("--retry-delay", type=str, help=f"Delay between image requests after getting a 503 from the first attempt (in seconds). Use 0 for no delay. Default: {config.retry_delay} second.")

    args = parser.parse_args()

    params = {
        "delay": args.delay,
        "retry_delay": args.retry_delay
    }

    config = load_config(args.conf, params)

    filename = downloader.download(args.manifest, args.zip_file_name, config.scratch_dir)

    print (f"Created {filename}")