import os

import unittest
from unittest.mock import patch
import json
import tempfile
from iiif_archive.downloader import download
from iiif_archive.processors import infoJson_factory
from tests.utils import mockResponse, MockAssetResponse

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

    def test_scale_factors(self):
        with open("tests/fixtures/2.0/level0-info.json", "r") as f:
            data = json.load(f)

            infoJson = infoJson_factory(data)

            urls = infoJson.scaleTiles(32, 1024, 1024)
            self.assertEqual(1, len(urls), "For scaleFactor 32")
            self.assertEqual("https://iiif-test.github.io/March2025/images/asna_1/full/119,/0/default.jpg", urls[0])

            urls = infoJson.scaleTiles(16, 1024, 1024)
            self.assertEqual(1, len(urls), "For scaleFactor 16")
            self.assertEqual("https://iiif-test.github.io/March2025/images/asna_1/full/238,/0/default.jpg", urls[0])

            urls = infoJson.scaleTiles(8, 1024, 1024)
            self.assertEqual(1, len(urls), "For scaleFactor 8")
            self.assertEqual("https://iiif-test.github.io/March2025/images/asna_1/full/475,/0/default.jpg", urls[0])

            urls = infoJson.scaleTiles(4, 1024, 1024)
            self.assertEqual(1, len(urls), "For scaleFactor 4")
            self.assertEqual("https://iiif-test.github.io/March2025/images/asna_1/full/949,/0/default.jpg", urls[0])

            urls = infoJson.scaleTiles(2, 1024, 1024)
            self.assertEqual(6, len(urls), "For scaleFactor 2")
            self.assertTrue("https://iiif-test.github.io/March2025/images/asna_1/0,0,2048,2048/1024,/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/March2025/images/asna_1/0,2048,2048,2048/1024,/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/March2025/images/asna_1/0,4096,2048,1111/1024,/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/March2025/images/asna_1/2048,0,1746,2048/873,/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/March2025/images/asna_1/2048,2048,1746,2048/873,/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/March2025/images/asna_1/2048,4096,1746,1111/873,/0/default.jpg" in urls)

            urls = infoJson.scaleTiles(1, 1024, 1024)
            self.assertEqual(24, len(urls), "For scaleFactor 1")
            self.assertTrue("https://iiif-test.github.io/March2025/images/asna_1/0,0,1024,1024/1024,/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/March2025/images/asna_1/0,1024,1024,1024/1024,/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/March2025/images/asna_1/0,2048,1024,1024/1024,/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/March2025/images/asna_1/0,3072,1024,1024/1024,/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/March2025/images/asna_1/0,4096,1024,1024/1024,/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/March2025/images/asna_1/0,5120,1024,87/1024,/0/default.jpg" in urls)

            self.assertTrue("https://iiif-test.github.io/March2025/images/asna_1/1024,0,1024,1024/1024,/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/March2025/images/asna_1/1024,1024,1024,1024/1024,/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/March2025/images/asna_1/1024,2048,1024,1024/1024,/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/March2025/images/asna_1/1024,3072,1024,1024/1024,/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/March2025/images/asna_1/1024,4096,1024,1024/1024,/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/March2025/images/asna_1/1024,5120,1024,87/1024,/0/default.jpg" in urls)

            self.assertTrue("https://iiif-test.github.io/March2025/images/asna_1/2048,0,1024,1024/1024,/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/March2025/images/asna_1/2048,1024,1024,1024/1024,/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/March2025/images/asna_1/2048,2048,1024,1024/1024,/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/March2025/images/asna_1/2048,3072,1024,1024/1024,/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/March2025/images/asna_1/2048,4096,1024,1024/1024,/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/March2025/images/asna_1/2048,5120,1024,87/1024,/0/default.jpg" in urls)

            self.assertTrue("https://iiif-test.github.io/March2025/images/asna_1/3072,0,722,1024/722,/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/March2025/images/asna_1/3072,1024,722,1024/722,/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/March2025/images/asna_1/3072,2048,722,1024/722,/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/March2025/images/asna_1/3072,3072,722,1024/722,/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/March2025/images/asna_1/3072,4096,722,1024/722,/0/default.jpg" in urls)
            self.assertTrue("https://iiif-test.github.io/March2025/images/asna_1/3072,5120,722,87/722,/0/default.jpg" in urls)

if __name__ == "__main__":
    unittest.main()