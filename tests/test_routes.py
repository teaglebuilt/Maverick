import pytest
from .utils import url


def test_basic_route(api):
    @api.route("/home")
    def home(request, response):
        response.text = "test home page"


def test_route_overlap_throws_exception(api):
    @api.route("/home")
    def home(req, resp):
        resp.text = "YOLO"

    with pytest.raises(AssertionError):
        @api.route("/home")
        def home2(req, resp):
            resp.text = "YOLO"


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