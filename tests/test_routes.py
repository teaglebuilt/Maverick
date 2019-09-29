import pytest
from .utils import url


def test_basic_route(api):
    @api.route("/home")
    def home(request, response):
        response.text = "test home page"


def test_parameterized_route(api, client):
    @api.route("/{name}")
    def hello(req, resp, name):
        resp.text = f"hey {name}"

    assert client.get("http://testserver/matthew").text == "hey matthew"
    assert client.get("http://testserver/ashley").text == "hey ashley"

def test_param_type_int_route(api, client):
    @api.route("/{age:d}")
    def age(request, response, age):
        response.text = f"Your age is {age}"

    assert client.get(url("/21")).text == "Your age is 21"


def test_add_route_method(api, client):
    EXPECTED_RESPONSE = "test worked"

    def test_handler(request, response):
        response.text = "test worked"

    api.add_route("/test_route", test_handler)
    assert client.get(url("/test_route")).text == EXPECTED_RESPONSE