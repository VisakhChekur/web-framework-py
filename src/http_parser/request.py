from http_parser.constants import HTTPMethods, HTTPVersions

class Request:
    def __init__(
        self,
        method: HTTPMethods,
        url: str,
        http_version: HTTPVersions,
        headers: dict[str, str] | None = None,
        data: bytes | None = None,
    ):

        self._method = method
        self.method = self._method
        self.url = url
        self._http_version = http_version
        self.http_version = self._http_version
        self.headers = headers
        self.raw = data
