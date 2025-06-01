import os

import unittest
from unittest.mock import patch
import json
import requests
import tempfile
from iiif_archive.downloader import download
from utils import mockResponse, MockAssetResponse

class TestVersion3(unittest.TestCase):
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
            if "manifest.json" in url:
                return mockResponse("tests/fixtures/3.0/0001-mvm-image.json")
            else:
                # doesn't matter for this test the wrong image is returned 
                return MockAssetResponse("tests/fixtures/assets/image.png")

        mockRequest.side_effect = mock_response    

        download("https://iiif.io/api/cookbook/recipe/0001-mvm-image/manifest.json", "simple_image3.zip", scratch=self.test_path, deleteScratch=False)

        self.assertTrue(os.path.exists(os.path.join(self.test_path, "simple_image3", "manifest.json")), "Expected to find manifest")
        self.assertTrue(os.path.exists(os.path.join(self.test_path, "simple_image3", "page1-full.png")), "Expected to find linked image")

        with open(os.path.join(self.test_path, "simple_image3", "manifest.json"), "r") as f:
            manifest = json.load(f)
            self.assertEqual("page1-full.png", manifest["items"][0]["items"][0]["items"][0]["body"]["id"], "Expected image resource id to be updated")

    @patch("requests.get")
    def test_simple_audio(self, mockRequest):
        # Define mock response for the specific URLs
        def mock_response(url, *args, **kwargs):
            if "manifest.json" in url:
                return mockResponse("tests/fixtures/3.0/0002-mvm-audio.json")
            else:
                # doesn't matter for this test the wrong audio is returned 
                return MockAssetResponse("tests/fixtures/assets/audio.wav")

        mockRequest.side_effect = mock_response    

        dir = "simple_audio"
        download("https://iiif.io/api/cookbook/recipe/0002-mvm-audio/manifest.json", f"{dir}.zip", scratch=self.test_path, deleteScratch=False)

        self.assertTrue(os.path.exists(os.path.join(self.test_path, dir, "manifest.json")), "Expected to find manifest")
        self.assertTrue(os.path.exists(os.path.join(self.test_path, dir, "128Kbps.mp4")), "Expected to find linked audio")

        with open(os.path.join(self.test_path, dir, "manifest.json"), "r") as f:
            manifest = json.load(f)
            self.assertEqual("128Kbps.mp4", manifest["items"][0]["items"][0]["items"][0]["body"]["id"], "Expected audio resource id to be updated")        

    @patch("requests.get")
    def test_simple_video(self, mockRequest):
        # Define mock response for the specific URLs
        def mock_response(url, *args, **kwargs):
            if "manifest.json" in url:
                return mockResponse("tests/fixtures/3.0/0003-mvm-video.json")
            else:
                # doesn't matter for this test the wrong audio is returned 
                return MockAssetResponse("tests/fixtures/assets/video.mp4")

        mockRequest.side_effect = mock_response    

        dir = "simple_video"
        download("https://iiif.io/api/cookbook/recipe/0003-mvm-video/manifest.json", f"{dir}.zip", scratch=self.test_path, deleteScratch=False)

        self.assertTrue(os.path.exists(os.path.join(self.test_path, dir, "manifest.json")), "Expected to find manifest")
        self.assertTrue(os.path.exists(os.path.join(self.test_path, dir, "lunchroom_manners_1024kb.mp4")), "Expected to find linked video")

        with open(os.path.join(self.test_path, dir, "manifest.json"), "r") as f:
            manifest = json.load(f)
            self.assertEqual("lunchroom_manners_1024kb.mp4", manifest["items"][0]["items"][0]["items"][0]["body"]["id"], "Expected video resource id to be updated")        

if __name__ == "__main__":
    unittest.main()