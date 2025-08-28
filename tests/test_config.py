import unittest

from iiif_archive.config import load_config


class TestConfig(unittest.TestCase):

    def test_defaults(self):
        config = load_config()

        self.assertEqual(config.delay, 1, "Setting from defaults should be 1")

    def test_fromfile(self):
        config = load_config("tests/test-config.ini")

        self.assertEqual(config.delay, 0, "Setting from test-config.ini should be 0")

    def test_cmdline(self):
        params = {
            "delay": 2
        }
        config = load_config("tests/test-config.ini", params)

        self.assertEqual(config.delay, 2, "Setting from command line should be 2")

    def test_emptycmdline(self):
        params = {}
        config = load_config("tests/test-config.ini", params)

        self.assertEqual(config.delay, 0, "Setting should be from provided properties file and equal to 0")
