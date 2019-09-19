import pytest
from api import API


@pytest.fixture
def api():
    return API()


def test_basic_route(api):
    @api.route("/home")
    def home(request, response):
        response.text = "test home page"