from typing import Tuple

from http_parser.request import Request
from http_parser.response import Response
from http_parser.typings import RequestLine
from http_parser.constants import methods, versions, HTTPMethods, HTTPVersions

"""
HTTP REQUEST FORMAT
-------------------
METHOD URL HTTP_VERSION\r\n
HEADERS\r\n
\r\n
DATA
"""


class HTTPParser:

    CARRIAGE_NEWLINE = b"\r\n"
    NEWLINE = b"\n"
    SPACE = b" "
    NEWLINE_INT = b"\n"[0]

    @staticmethod
    def deserialize_request(request: bytes) -> Request:

        request_line_end = request.find(HTTPParser.CARRIAGE_NEWLINE)
        request_line_details = _parse_request_line(request[:request_line_end])
        headers_start = request_line_end + 2  # Skipping the \r\n

        # No headers
        if request[headers_start:headers_start+2] == HTTPParser.CARRIAGE_NEWLINE:
            headers = None
            # Add 2 to ignore the \r\n
            data_start = headers_start + 2
        else:
            # The returned data_start is the index of the start of the
            # data with respect to the start of the headers since
            # only the data from headers onwards is being passed
            headers, data_start = _parse_headers(request[headers_start:])
            data_start += headers_start

        # No data
        if data_start >= len(request):
            data = None
        else:
            data = request[data_start:]

        return Request(
            request_line_details["method"],
            request_line_details["url"],
            request_line_details["version"],
            headers=headers,
            data=data,
        )

    @staticmethod
    def serialize_response(response: Response) -> bytes:

        serialized_resp: list[bytes] = []
        serialized_resp.append(_serialize_status_line(response))

        if response.headers:
            serialized_resp.append(_serialize_headers(response.headers))
        serialized_resp.append(HTTPParser.CARRIAGE_NEWLINE)

        if response.raw:
            serialized_resp.append(response.raw)

        return b"".join(serialized_resp)


def _serialize_status_line(response: Response) -> bytes:

    status_line: list[bytes] = []
    status_line_values: list[str] = [
        response.version.value, str(response.status_code), response.phrase]
    for status in status_line_values:
        status_line.append(bytes(status, encoding="ascii"))
        status_line.append(HTTPParser.SPACE)
    status_line[-1] = HTTPParser.CARRIAGE_NEWLINE
    return b"".join(status_line)


def _serialize_headers(headers: dict[str, str]) -> bytes:

    serialized_headers: list[bytes] = []
    for name, value in headers.items():
        serialized_headers.append(bytes(name + ":", encoding="ascii"))
        serialized_headers.append(HTTPParser.SPACE)
        serialized_headers.append(bytes(value, encoding="ascii"))
        serialized_headers.append(HTTPParser.CARRIAGE_NEWLINE)
    return b"".join(serialized_headers)


def _parse_headers(req: bytes) -> Tuple[dict[str, str], int]:

    headers: dict[str, str] = {}
    header_end = req.find(HTTPParser.CARRIAGE_NEWLINE)
    header_start = 0
    while True:
        header = req[header_start:header_end]
        name_value_seperator_idx = header.find(HTTPParser.SPACE)
        # Subtract 1 to get rid of the ':'
        header_name = str(
            header[: name_value_seperator_idx - 1], encoding="ascii")
        # Add 1 to not include the space
        header_value = str(
            header[name_value_seperator_idx + 1:], encoding="ascii")
        headers[header_name] = header_value
        header_start = header_end + 2  # Skipping \r\n
        # Marks the end of the headers
        if req[header_start:header_start+2] == HTTPParser.CARRIAGE_NEWLINE:
            break
        header_end = req.find(HTTPParser.CARRIAGE_NEWLINE, header_start)
    # Header start would be the '\r\n' after the headers
    # Add 2 to that to get the starting index of the data if
    # present
    return (headers, header_start + 2)


def _parse_request_line(request_line: bytes) -> RequestLine:

    method_end = request_line.find(HTTPParser.SPACE)
    method = methods.get(request_line[:method_end], HTTPMethods.UNKNOWN)
    url_end = request_line.find(HTTPParser.SPACE, method_end + 1)
    url = str(request_line[method_end + 1: url_end], encoding="ascii")
    version = versions.get(request_line[url_end + 1:], HTTPVersions.UNKNOWN)

    request_line_parsed: RequestLine = {
        "method": method,
        "url": url,
        "version": version,
    }
    return request_line_parsed
