# iiif-archive
Creates a backup of a IIIF Manifest with images

## Download manifest and create zip:

```
python deflate.py -h
usage: deflate.py [-h] [--zip-file-name ZIP_FILE_NAME] [--conf CONF] manifest

Download a Manifest and store the results in a zip file

positional arguments:
  manifest              https URL to the manifest

options:
  -h, --help            show this help message and exit
  --zip-file-name ZIP_FILE_NAME
                        Name of the zip file (default: manifest.zip)
  --conf CONF           Config file
```

Example:
```
python deflate.py -zip-file-name simple_image3 https://iiif.io/api/cookbook/recipe/0001-mvm-image/manifest.json
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