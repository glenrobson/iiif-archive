import os

import unittest
from unittest.mock import patch
import json
import tempfile
from iiif_archive.downloader import download
from iiif_archive.processors import infoJson_factory
from tests.utils import mockResponse, MockAssetResponse
from iiif_archive.config import get_config, load_config

class TestVersion3(unittest.TestCase):
    def setUp(self) -> None:
        # Set up config
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_path = self.temp_dir.name
        config = load_config("tests/test-config.ini")

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


    @patch("requests.get")
    def test_iiif_image(self, mockRequest):
        # Define mock response for the specific URLs
        def mock_response(url, *args, **kwargs):
            if "manifest.json" in url:
                return mockResponse("tests/fixtures/3.0/0005-image-service.json")
            elif "info.json" in url:
                # doesn't matter for this test the wrong audio is returned 
                return mockResponse("tests/fixtures/3.0/gottingen-info.json")
            else:
                return MockAssetResponse("tests/fixtures/assets/image.png")    

        mockRequest.side_effect = mock_response    

        dir = "iiif_image3"
        download("https://iiif.io/api/cookbook/recipe/0005-image-service/manifest.json", f"{dir}.zip", scratch=self.test_path, deleteScratch=False)

        self.assertTrue(os.path.exists(os.path.join(self.test_path, dir, "manifest.json")), "Expected to find manifest")
        imageDir = os.path.join(self.test_path, dir, "918ecd18c2592080851777620de9bcb5-gottingen")
        self.assertTrue(os.path.exists(imageDir), "Expected to find linked IIIF image")
        self.assertTrue(os.path.isdir(imageDir), "Expected image to be a directory")
        self.assertTrue(os.path.exists(os.path.join(imageDir, "info.json")), "Expected to find info.json")

        self.assertTrue(os.path.exists(os.path.join(imageDir, "0,0,2048,2048/512,512/0/default.jpg")), "Expected to find scaleFactor 4")
        self.assertTrue(os.path.exists(os.path.join(imageDir, "0,0,1024,1024/512,512/0/default.jpg")), "Expected to find scaleFactor 2")
        self.assertTrue(os.path.exists(os.path.join(imageDir, "0,0,512,512/512,512/0/default.jpg")), "Expected to find scaleFactor 1")

        with open(os.path.join(self.test_path, dir, "manifest.json"), "r") as f:
            manifest = json.load(f)
            self.assertEqual("918ecd18c2592080851777620de9bcb5-gottingen", manifest["items"][0]["items"][0]["items"][0]["body"]["service"][0]["id"], "Expected IIIF image id to be updated")        


    def test_scale_factors(self):
        with open("tests/fixtures/3.0/level0-info.json", "r") as f:
            data = json.load(f)

            infoJson = infoJson_factory(data)

            urls = infoJson.scaleTiles(32, 1024, 1024)
            self.assertEqual(1, len(urls), "For scaleFactor 32")
            self.assertEqual("https://iiif-test.github.io/actions_test/images/IMG_5954/full/126,95/0/default.jpg", urls[0])

            urls = infoJson.scaleTiles(16, 1024, 1024)
            self.assertEqual(1, len(urls), "For scaleFactor 16")
            self.assertEqual("https://iiif-test.github.io/actions_test/images/IMG_5954/full/252,189/0/default.jpg", urls[0])

            urls = infoJson.scaleTiles(8, 1024, 1024)
            self.assertEqual(1, len(urls), "For scaleFactor 8")
            self.assertEqual("https://iiif-test.github.io/actions_test/images/IMG_5954/full/504,378/0/default.jpg", urls[0])

            urls = infoJson.scaleTiles(4, 1024, 1024)
            self.assertEqual(1, len(urls), "For scaleFactor 4")
            self.assertEqual("https://iiif-test.github.io/actions_test/images/IMG_5954/full/1008,756/0/default.jpg", urls[0])

            urls = infoJson.scaleTiles(2, 1024, 1024)
            self.assertEqual(4, len(urls), "For scaleFactor 2")
            self.assertTrue("https://iiif-test.github.io/actions_test/images/IMG_5954/0,0,2048,2048/1024,1024/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/actions_test/images/IMG_5954/2048,0,1984,2048/992,1024/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/actions_test/images/IMG_5954/0,2048,2048,976/1024,488/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/actions_test/images/IMG_5954/2048,2048,1984,976/992,488/0/default.jpg" in urls)

            urls = infoJson.scaleTiles(1, 1024, 1024)
            self.assertEqual(12, len(urls), "For scaleFactor 1")
            self.assertTrue("https://iiif-test.github.io/actions_test/images/IMG_5954/0,0,1024,1024/1024,1024/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/actions_test/images/IMG_5954/0,1024,1024,1024/1024,1024/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/actions_test/images/IMG_5954/0,2048,1024,976/1024,976/0/default.jpg" in urls)

            self.assertTrue("https://iiif-test.github.io/actions_test/images/IMG_5954/1024,0,1024,1024/1024,1024/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/actions_test/images/IMG_5954/1024,1024,1024,1024/1024,1024/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/actions_test/images/IMG_5954/1024,2048,1024,976/1024,976/0/default.jpg" in urls)

            self.assertTrue("https://iiif-test.github.io/actions_test/images/IMG_5954/2048,0,1024,1024/1024,1024/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/actions_test/images/IMG_5954/2048,1024,1024,1024/1024,1024/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/actions_test/images/IMG_5954/2048,2048,1024,976/1024,976/0/default.jpg" in urls)

            self.assertTrue("https://iiif-test.github.io/actions_test/images/IMG_5954/3072,0,960,1024/960,1024/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/actions_test/images/IMG_5954/3072,1024,960,1024/960,1024/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/actions_test/images/IMG_5954/3072,2048,960,976/960,976/0/default.jpg" in urls)

    def test_level0(self):
        with open("tests/fixtures/3.0/level0-info.json", "r") as f:
            data = json.load(f)
            infoJson = infoJson_factory(data)

            self.assertTrue(infoJson.isLevel0(), "Expected to find level 0 image")

        with open("tests/fixtures/3.0/gottingen-info.json", "r") as f:
            data = json.load(f)
            infoJson = infoJson_factory(data)

            self.assertFalse(infoJson.isLevel0(), "Image is not a level 0 image")
if __name__ == "__main__":
    unittest.main()