from http import HTTPStatus
import traceback


def debug_exception_handler(req, resp, exception):
    resp.text = f"{exception}\n\n{traceback.format_exc()}"

    

class HTTPError(Exception):

    def __init__(self, status: int):
        assert isinstance(status, int), "Status should be an integer"
        self._http_status = HTTPStatus(status)

    @property
    def status(self):
        return self._http_status.value

    @property
    def status_phrase(self):
        return self._http_status.phrase

    def __str__(self):
        return f"{self.status} {self.status_phrase}"