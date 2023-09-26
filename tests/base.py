from fastapi.testclient import TestClient

from twitter import config


def db_uri_patch():
    print('Getting')
    return 'postgresql+psycopg2://'


config.get_postgres_uri = db_uri_patch

from twitter.entrypoints.fastapi_app import app

client = TestClient(app)
