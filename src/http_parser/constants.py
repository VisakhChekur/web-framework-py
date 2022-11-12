from enum import Enum


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


methods = {
    b"GET": HTTPMethods.GET,
    b"POST": HTTPMethods.POST,
    b"PUT": HTTPMethods.PUT,
    b"DELETE": HTTPMethods.DELETE,
    b"UNKNOWN": HTTPMethods.UNKNOWN,
}
versions = {
    b"HTTP/1": HTTPVersions.HTTP_1,
    b"HTTP/1.1": HTTPVersions.HTTP_1_1,
    b"HTTP/2": HTTPVersions.HTTP_2,
    b"HTTP/3": HTTPVersions.HTTP_3,
    b"UNKNOWN": HTTPVersions.UNKNOWN,
}

status_codes_phrases = {
    200: "OK",
    404: "Not Found",
    500: "Internal Server Error"
}

# Ensure that the members in the enums and the dictionary are
# in sync
assert set(methods.keys()) == {
    bytes(member.value, encoding="utf-8") for member in HTTPMethods
}, "methods dictionary doesn't match HTTPMethods enum"
assert set(versions.keys()) == {
    bytes(member.value, encoding="utf-8") for member in HTTPVersions
}, "versions dictionary doesn't match HTTPVersions enum"
