import socket


# This is a proof of concept to see if we can eliminate gunicorn and WebOb as a dependency.

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def format_headers(headers):
    obj = dict()
    for key, value in headers.items():
        obj[key] = f"HTTP_{key}"
        obj[value] = value
    return obj
    

def parse_request(http):
    request, *headers, _, body = http.split('\r\n')
    method, path, protocol = request.split(' ')
    headers = dict(
        line.split(':', maxsplit=1)
        for line in headers
    )
    return method, path, headers, protocol, body


def process_response():
    return (

    )


def to_environ(method, path, headers, protocol, body):
    return {
        "REQUEST_METHOD": method,
        "PATH_INFO": path,
        "SERVER_PROTOCOL": protocol,
        "wsgi.input": StringIO(body),
        **format_headers(headers)
    }


with socket.socket() as s:
    s.bind(('localhost', 8000))
    s.listen(1)
    conn, addr = s.accept()

    while True:
        with conn:
            http_request = conn.recv(1024).decode('utf-8')
            request = parse_request(http_request)
            environ = to_environ(*request)
            print(environ)
            conn.send_all("Hello World".encode('utf-8'))