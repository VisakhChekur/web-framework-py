from exceptions.exceptions import MethodNotImplemented
from http_parser.request import Request
from http_parser.response import Response


class BaseController:

    path = ""

    def get(self, req: Request, resp: Response) -> None:
        raise MethodNotImplemented("GET")

    def post(self, req: Request, resp: Response) -> None:
        raise MethodNotImplemented("POST")

    def put(self, req: Request, resp: Response) -> None:
        raise MethodNotImplemented("PUT")

    def delete(self, req: Request, resp: Response) -> None:
        raise MethodNotImplemented("DELETE")

    def __init_subclass__(cls) -> None:

        for method_name in ("get", "post", "put", "delete"):
            method = getattr(cls, method_name)
            if not callable(method):
                raise TypeError(
                    f"'{method}' in '{cls.__name__}' must be a callable")
            if method.__code__.co_argcount != 3:
                raise TypeError(
                    f"'{method_name}' in '{cls.__name__}' must take exactly 3 arguments: self, request: Request, response: Response")
