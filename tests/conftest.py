from src.maverick import API
import pytest


@pytest.fixture
def api():
    return API()


@pytest.fixture
def client(api):
    return api.session()