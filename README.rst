Maverick
========

$This is a python framework using Gunicorn as the WSGI HTTP Server. The goal is to write a lightweight framework capable of
a production environment.

$As of now, there is a callable object that expects two parameters "environ" && start_response".
Then returns a WSGI compatible response 

Look how easy it is to use:

    from api import API

    app = API()

    @app.route('/')
    def home(request, response):
	    response.text = "Hello from home page"

    @app.route('/about')
    def about(request, response):
	    response.text = "Hello from the About Page"