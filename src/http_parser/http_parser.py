
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
    HEADER_DELIMITER = b": "
    DOUBLE_CARRIAGE_NEWLINE = b"\r\n\r\n"
    SPACE = b" "

    @staticmethod
    def deserialize_request(request: bytes) -> Request:

        request_metadata, data = request.split(
            HTTPParser.DOUBLE_CARRIAGE_NEWLINE, 1)
        request_metadata_lines = request_metadata.split(
            HTTPParser.CARRIAGE_NEWLINE)
        request_line_details = _parse_request_line(request_metadata_lines[0])
        headers = _parse_headers(request_metadata_lines[1:])

        return Request(
            request_line_details["method"],
            request_line_details["url"],
            request_line_details["version"],
            headers=headers if headers else None,
            data=data if data else None,
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


def _parse_headers(headers: list[bytes]) -> dict[str, str]:

    parsed_headers: dict[str, str] = {}
    for header in headers:
        header_components = [str(component, encoding="ascii")
                             for component in header.split(HTTPParser.HEADER_DELIMITER, 1)]
        parsed_headers[header_components[0]] = header_components[1]
    return parsed_headers


def _parse_request_line(request_line: bytes) -> RequestLine:

    components = request_line.split()
    request_line_parsed: RequestLine = {
        "method": methods.get(components[0], HTTPMethods.UNKNOWN),
        "url": str(components[1], encoding="ascii"),
        "version": versions.get(components[2], HTTPVersions.UNKNOWN),
    }
    return request_line_parsed
