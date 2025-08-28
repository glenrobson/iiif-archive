# iiif-archive
Creates a backup of a IIIF Manifest with images

## Download manifest and create zip:
To create a zip file of a manifest you can run deflate:

```
usage: deflate.py [-h] [--zip-file-name ZIP_FILE_NAME] [--conf CONF] [--delay DELAY] [--retry-delay RETRY_DELAY] manifest

Download a Manifest and store the results in a zip file

positional arguments:
  manifest              https URL to the manifest

options:
  -h, --help            show this help message and exit
  --zip-file-name ZIP_FILE_NAME
                        Name of the zip file (default: manifest.zip)
  --conf CONF           Config file. Default: conf/config.ini
  --delay DELAY         Delay between image requests in seconds. Use 0 for no delay. Default: 1 second.
  --retry-delay RETRY_DELAY
                        Delay between image requests after getting a 503 from the first attempt (in seconds). Use 0 for no delay. Default: 1 second.
```

Example:
```
python deflate.py -zip-file-name simple_image3 https://iiif.io/api/cookbook/recipe/0001-mvm-image/manifest.json
```
To turn this zip file into a directory of files that you can host on a web server you can use inflate:

```
python inflate.py -h 
usage: inflate.py [-h] zip_file local_dir base_url

Export a zipped Manifest so it can be served at a specified URL

positional arguments:
  zip_file    zip_file to inflate
  local_dir   directory to inflate zip file to
  base_url    base URL that the manifest will be served at

options:
  -h, --help  show this help message and exit
```

Example:

```
python inflate.py ScottishClans.zip  iiif_stuff/ https://glenrobson.github.io/iiif_stuff/
```

## Running tests

```
python -m unittest discover -s tests
```
Run a single test:

```
python -m unittest tests.test_version3.TestVersion3.test_iiif_image
```

## Test fixtures

Create test image:

```
pip install pillow
```

```
python tests/fixtures/createTestImage.py
```

Create test audio:

```
pip install scipy
pip install numpy
```

```
python tests/fixtures/createTestAudio.py
```

Create test video:
```
pip install numpy
pip install opencv-python
```

```
python tests/fixtures/createTestVideo.py
```