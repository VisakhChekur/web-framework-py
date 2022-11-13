from http import HTTPStatus
from http_parser.constants import HTTPVersions
from http_parser.response import Response


class NotFound(Response):

    def __init__(self, version: HTTPVersions):

        super().__init__(version, {}, HTTPStatus.NOT_FOUND)


class MethodNotAllowed(Response):

    def __init__(self, version: HTTPVersions):

        super().__init__(version, {}, HTTPStatus.METHOD_NOT_ALLOWED)


class InternalServerError(Response):
    def __init__(self, version: HTTPVersions):

        super().__init__(version, {}, HTTPStatus.INTERNAL_SERVER_ERROR)
