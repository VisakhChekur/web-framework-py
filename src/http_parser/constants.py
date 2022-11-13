from enum import Enum
from http import HTTPStatus


class HTTPVersions(Enum):

    HTTP_1 = "HTTP/1"
    HTTP_1_1 = "HTTP/1.1"
    HTTP_2 = "HTTP/2"
    HTTP_3 = "HTTP/3"
    UNKNOWN = "UNKNOWN"


class HTTPMethods(Enum):

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    UNKNOWN = "UNKNOWN"


METHODS_MAPPING_STR = {member.value: member for member in HTTPMethods}
METHODS_MAPPING_BYTES = {
    bytes(member.value, encoding="ascii"): member for member in HTTPMethods}
VERSIONS_MAPPING = {bytes(member.value, encoding="ascii")                    : member for member in HTTPVersions}
STATUS_CODE_MAPPING = {member.value: member for member in HTTPStatus}
