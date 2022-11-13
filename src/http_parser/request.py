import json
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
        self.headers = headers if headers else {}
        self.raw = data if data else b""
        self._json = None

    @property
    def json(self):
        
        if self._json:
            return self._json
    
        content_type = self.headers.get("Content-Type", None)
        if content_type != "application/json":
            raise TypeError("request data is not of mime type application/json")
        return json.loads(self.raw)
