===========================
MAVERICK
===========================

This is a `Python <http://python.org/>` web framework in the making:

As of now, there is a callable object that expects two parameters "environ" && start_response".
Then returns a WSGI compatible response 

Look how easy it is to use:

.. code-block:: python

    from api import API

    app = API()

    @app.route('/')
    def home(request, response):
	    response.text = "Hello from home page"

    @app.route('/about')
    def about(request, response):
	    response.text = "Hello from the About Page"
