from typing import TypedDict


from http_parser.constants import HTTPMethods, HTTPVersions


class RequestLine(TypedDict):

    url: str
    method: HTTPMethods
    version: HTTPVersions
