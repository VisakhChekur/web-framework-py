import json
from typing import Any

from http_parser.constants import HTTPVersions, status_codes_phrases

"""
HTTP RESPONE FORMAT
-------------------
version status_code phrase\r\n
headers\r\n
\n
data
"""


class Response:

    def __init__(self, version: HTTPVersions, headers: dict[str, str] | None = None):

        self.version = version
        self.data: Any = None
        self._status_code = 200
        self.phrase = "OK"
        self.headers = {
            "Content-Type": "text/html",
        }

    @property
    def status_code(self):

        return self._status_code

    @status_code.setter
    def status_code(self, status_code: int):

        try:
            self.phrase = status_codes_phrases[status_code]
        except KeyError:
            raise ValueError("invalid status code given")
        self._status_code = status_code

    @property
    def raw(self) -> bytes:
        return self._data_to_bytes()

    def _data_to_bytes(self):

        if not self.data:
            return b""

        if self.headers["Content-Type"] == "text/html":
            try:
                # DOUBT: Are 'text/html' encoded in UTF-8?
                return bytes(self.data, encoding="utf-8")
            except TypeError:
                raise TypeError(
                    f"'data' must be of type 'str' if content type is text/html")

        if self.headers["Content-Type"] == "application/json":
            json_str = json.dumps(self.data)
            return bytes(json_str, encoding="utf-8")

        raise ValueError("invalid Content-Type")
