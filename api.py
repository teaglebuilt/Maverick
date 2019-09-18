from webob import Request, Response

class API:

    def __init__(self):
        self.routes = {}

    def route(self, path):
        def wrapper(handler):
            self.routes[path] = handler
            print(self.routes)
            return handler
        return wrapper

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def default_response(self, response):
        response.status_code = 404
        response.text = "Not Found"
        
    def handle_request(self, request):
        response = Response()
        print(request.path)
        for path, handler in self.routes.items():
            if path == request.path:
                handler(request, response)
                return response
        self.default_response(response)
        return response
    