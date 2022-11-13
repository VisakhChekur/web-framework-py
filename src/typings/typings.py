from typing import TypedDict, Callable
from http_parser.constants import HTTPMethods

ROUTED_METHOD = Callable[..., None]


class RoutedMethodDetails(TypedDict):

    func: ROUTED_METHOD
    methods: list[HTTPMethods]
