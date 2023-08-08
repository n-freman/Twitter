from fastapi.testclient import TestClient

from twitter.entrypoints.fastapi_app import app

client = TestClient(app)
