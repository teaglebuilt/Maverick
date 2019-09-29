from webob import Request, Response
from parse import parse
import inspect, os
from requests import session as RequestsSession
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter
from .templates import get_templates_env


class API:

    def __init__(self, templates_dir="templates"):
        self.routes = {}
        self.templates = get_templates_env(os.path.abspath(templates_dir))
        self.exception_handler = None
        # cached request session
        self._session = None

    def route(self, pattern):
        """ ADD ROUTE """
        def wrapper(handler):
            self.add_route(pattern, handler)
            return handler

        return wrapper

    def add_route(self, pattern, handler):

        assert pattern not in self.routes, "This path already exists"

        self.routes[pattern] = handler

    def template(self, name, context):
        return self.templates.get_template(name).render(**context)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def default_response(self, response):
        response.status_code = 404
        response.text = "Not Found"

    def dispatch_request(self, request):
        response = Response()
        handler, kwargs = self.find_handler(request_path=request.path)

        if handler is not None:
            if inspect.isclass(handler):
                handler = getattr(handler(), request.method.lower(), None)
                if handler is None:
                    raise AttributeError("Method now allowed", request.method)

            handler(request, response, **kwargs)
        else:
            self.default_response(response)
        return response

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named
        return None, None

    def session(self, base_url="http://testserver"):
        if self._session is None:
            session = RequestsSession()
            session.mount(prefix=base_url, adapter=RequestsWSGIAdapter(self))
            self._session = session
        return self._session

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)
