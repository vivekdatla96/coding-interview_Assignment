import pytest
from api.app import create_app

@pytest.fixture(scope="session")
def app():
    app = create_app(testing=True)
    return app

@pytest.fixture(scope="session")
def client(app):
    return app.test_client()
