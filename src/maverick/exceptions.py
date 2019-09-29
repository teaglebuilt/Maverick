from http import HTTPStatus


class HTTPError(Exception):

    def __init__(self, status: int):
        self._http_status = HTTPStatus(status)