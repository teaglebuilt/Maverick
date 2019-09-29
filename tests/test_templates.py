import pytest


def test_render_template_in_handler(api):
    EXPECTED_RESPONSE = {"title": "Test title", "body": "Testing body content"}
    
    @api.route('/show/template')
    def handler_with_template(request, response):
	    response.text = app.template("example.html", context={"title": "Test title", "body": "Testing body content"})
	    response.content_type = "text/html"
