import os

import unittest
from unittest.mock import patch
import json
import requests
import tempfile
from iiif_archive.downloader import download
from utils import mockResponse, MockAssetResponse

class TestVersion2(unittest.TestCase):
    def setUp(self) -> None:
        # Set up config
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_path = self.temp_dir.name

    def tearDown(self):
        return self.temp_dir.cleanup();    

    @patch("requests.get")
    def test_simple_image(self, mockRequest):
        # Define mock response for the specific URLs
        def mock_response(url, *args, **kwargs):
            if "manifest2.json" in url:
                return mockResponse("tests/fixtures/2.0/simple_image.json")
            else:
                return MockAssetResponse("tests/fixtures/assets/image.png")

        mockRequest.side_effect = mock_response    

        download("https://glenrobson.github.io/iiif_stuff/simple_images/manifest2.json", "simple_image2.zip", scratch=self.test_path, deleteScratch=False)

        self.assertTrue(os.path.exists(os.path.join(self.test_path, "simple_image2", "manifest.json")), "Expected to find manifest")
        self.assertTrue(os.path.exists(os.path.join(self.test_path, "simple_image2", "gottingen.jpg")), "Expected to find linked image")

        with open(os.path.join(self.test_path, "simple_image2", "manifest.json"), "r") as f:
            manifest = json.load(f)
            self.assertEqual("gottingen.jpg", manifest["sequences"][0]["canvases"][0]["images"][0]["resource"]["@id"], "Expected image resource id to be updated")

if __name__ == "__main__":
    unittest.main()