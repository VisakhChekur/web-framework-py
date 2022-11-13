import logging
from socket import socket

from http_parser.constants import HTTPMethods
from http_parser.response import Response
from http_parser.request import Request
from server.server import make_server, Server
from server.socket_request import SocketMessage
from base_controller import BaseController
from http_parser.http_parser import HTTPParser
from url_parser.url_parser import parse_url
from exceptions.exceptions import MethodNotImplemented
from default_response import default_responses

TCP_CONNECTIONS_LIMIT = 5
HOSTNAME = ''
PORT = 80


class App:

    def __init__(self):

        self._controllers: dict[str, BaseController] = {}

    def run(self):

        with make_server() as server:

            server.receive(HOSTNAME, PORT, TCP_CONNECTIONS_LIMIT)
            while True:
                rec_msg = server.get_message()
                request = HTTPParser.deserialize_request(rec_msg.message)
                response = self._route_request(request)
                self._send_response(response, rec_msg.conn)

    def register_controllers(self, *controllers: BaseController):

        for controller in controllers:
            if not isinstance(controller, BaseController):  # type: ignore
                raise TypeError(
                    f"controller must be an instance of a class that inherits from BaseController")
            controller_name = controller.__class__.__name__.lower()
            if controller_name == "home":
                controller_name = ""
            self._controllers[controller_name] = controller

    def _route_request(self, request: Request) -> Response:
        """Routes the request to the correct controller and method."""

        try:
            parsed_url = parse_url(request.url)
            controller = self._controllers[parsed_url.controller_path]
            http_method = self._get_http_method(request.method, controller)
            resp = Response(request.http_version)
            http_method(request, resp)
            return resp
        except KeyError:
            return default_responses.NotFound(request.http_version)
        except MethodNotImplemented:
            return default_responses.MethodNotAllowed(request.http_version)
        except Exception as e:
            logging.exception(e)
            return default_responses.InternalServerError(request.http_version)

    def _get_http_method(self, http_method: HTTPMethods, controller: BaseController):

        match http_method.value:
            case "GET":
                return controller.get
            case "POST":
                return controller.post
            case "PUT":
                return controller.put
            case "DELETE":
                return controller.delete
            case _:
                raise MethodNotImplemented("")

    def _send_response(self, resp: Response, conn: socket):

        deserialized_resp = HTTPParser.serialize_response(resp)
        resp_msg = SocketMessage(conn, ("", 0), deserialized_resp)
        Server.send_message(resp_msg)


"""
1. Parse the request
2. Parse the url to get the controller
3. 
"""
