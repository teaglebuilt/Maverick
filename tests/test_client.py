import pytest
from .utils import url


def test_client_can_send_requests(api, client):
    RESPONSE_TEXT = "THIS IS COOL"

    @api.route("/hey")
    def cool(req, resp):
        resp.text = RESPONSE_TEXT

    assert client.get(url("/hey")).text == RESPONSE_TEXT


def test_default_404_response(client):
    response = client.get(url("/doesnotexist"))

    assert response.status_code == 404
    assert response.text == "Not Found"


def test_class_based_handler_post(api, client):
    RESPONSE_TEXT = "this is a post request"

    @api.route("/post")
    class PostHandler:

        def post(self, request, response):
            response.text = "this is a post request"

    assert client.post(url("/post")).text == RESPONSE_TEXT

def test_class_based_handler_not_allowed_method(api, client):
    @api.route("/post")
    class BookResource:
        def post(self, request, response):
            resp.text = "this is not allowed"

    with pytest.raises(AttributeError):
        client.get(url("/post"))