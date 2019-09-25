from webob import Request, Response
from parse import parse
import inspect, os
from requests import session as RequestsSession
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter
from jinja2 import Environment, FileSystemLoader


def get_templates_env(templates_dir):
    return Environment(loader=FileSystemLoader(templates_dir), autoescape=(["html", "xml"]))


class API:

    def __init__(self, templates_dir="templates"):
        self.routes = {}
        self.templates = get_templates_env(os.path.abspath(templates_dir))
        # cached request session
        self._session = None

    def route(self, pattern):
        """ ADD ROUTE """
        assert pattern not in self.routes
            
        def wrapper(handler):
            self.routes[pattern] = handler
            return handler

        return wrapper

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
