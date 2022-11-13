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


METHODS_MAPPING = {bytes(member.value, encoding="ascii")
                         : member for member in HTTPMethods}
VERSIONS_MAPPING = {bytes(member.value, encoding="ascii")
                          : member for member in HTTPVersions}
STATUS_CODE_MAPPING = {member.value: member for member in HTTPStatus}

# Ensure that the members in the enums and the dictionary are
# in sync
assert set(METHODS_MAPPING.keys()) == {
    bytes(member.value, encoding="utf-8") for member in HTTPMethods
}, "methods dictionary doesn't match HTTPMethods enum"
assert set(VERSIONS_MAPPING.keys()) == {
    bytes(member.value, encoding="utf-8") for member in HTTPVersions
}, "versions dictionary doesn't match HTTPVersions enum"
