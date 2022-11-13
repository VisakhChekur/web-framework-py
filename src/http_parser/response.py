import json
from typing import Any

from http_parser.constants import HTTPVersions, STATUS_CODE_MAPPING
from http import HTTPStatus

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
        self._status_code = HTTPStatus.OK
        self.headers = {
            "Content-Type": "text/html",
        }

    @property
    def status_code(self):

        return self._status_code.value

    @status_code.setter
    def status_code(self, status_code: int):

        try:
            self._status_code = STATUS_CODE_MAPPING[status_code]
        except KeyError:
            raise ValueError("invalid status code given")

    @property
    def raw(self) -> bytes:
        return self._data_to_bytes()

    def _data_to_bytes(self):

        if not self.data:
            return b""

        if self.headers["Content-Type"] == "text/html" or self.headers["Content-Type"] == "text/plain":
            try:
                # DOUBT: Are 'text/html' encoded in UTF-8?
                return bytes(self.data, encoding="utf-8")
            except TypeError:
                raise TypeError(
                    f"'data' must be of type 'str' if content type is text/html")

        if self.headers["Content-Type"] == "application/json":
            json_bytes = bytes(json.dumps(self.data), encoding="utf-8")
            self.headers["Content-Length"] = str(len(json_bytes))
            return json_bytes

        raise ValueError("invalid Content-Type")
