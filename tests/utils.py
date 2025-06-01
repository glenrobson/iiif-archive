import json
import requests

def mockResponse(fixture):
    class MockResponse:
        status_code = 200
        def json(self):
            with open(fixture, "r") as file:
                return json.load(file)

        def raise_for_status(self):
            return        

    return MockResponse()

# Your mock response class
class MockAssetResponse:
    def __init__(self, file_path, status_code=200):
        self.file_path = file_path
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} Error")

    def iter_content(self, chunk_size=8192):
        with open(self.file_path, "rb") as f:
            while chunk := f.read(chunk_size):
                yield chunk

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()