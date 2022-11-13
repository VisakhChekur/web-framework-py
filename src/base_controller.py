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
