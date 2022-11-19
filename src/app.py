import functools
import logging
from socket import socket
from typing import Any, Callable

from base_controller import BaseController
from default_response import default_responses
from exceptions.exceptions import MethodNotImplemented
from http_parser.constants import METHODS_MAPPING_STR, HTTPMethods
from http_parser.http_parser import HTTPParser
from http_parser.request import Request
from http_parser.response import Response
from server.server import Server, make_server
from server.socket_request import SocketMessage
from typings.typings import ROUTED_METHOD, RoutedMethodDetails
from url_parser.url_parser import parse_url

TCP_CONNECTIONS_LIMIT = 5
HOSTNAME = ''
PORT = 80


class App:

    def __init__(self):

        self._controllers: dict[str, BaseController] = {}
        # Controller -> path -> RoutedMethodDetails
        self._routes: dict[str, dict[str, RoutedMethodDetails]] = {}

    def run(self):

        with make_server() as server:

            server.receive(HOSTNAME, PORT, TCP_CONNECTIONS_LIMIT)
            while True:
                rec_msg = server.get_message()
                request = HTTPParser.deserialize_request(rec_msg.message)
                response = self._route_request(request)
                self._send_response(response, rec_msg.conn)

    def route(self, path: str = "", methods: list[str] | None = None) -> Callable[..., ROUTED_METHOD]:

        def decorator(func: ROUTED_METHOD) -> ROUTED_METHOD:
            self._register_path(path, methods, func)

            @functools.wraps(func)
            def wrapped(*args: Any, **kwargs: Any):
                func(*args, **kwargs)
            return wrapped
        return decorator

    def register_controllers(self, *controllers: BaseController):

        for controller in controllers:
            if not isinstance(controller, BaseController):  # type: ignore
                raise TypeError(
                    f"controller must be an instance of a class that inherits from BaseController")
            controller_name = controller.__class__.__name__.lower()
            self._controllers[controller_name] = controller

    def _register_path(self, path: str, methods: list[str] | None, func: ROUTED_METHOD):
        """Maps the given function to the path in the implied controller."""

        class_name = self._get_class_name(func)
        mapped_methods = self._methods_path_register(methods, func)

        # This is a shit name. Idk a better way to name it.
        class_in_route = self._routes.setdefault(class_name, {})

        # Remove trailing '/'
        if path.startswith("/"):
            path = path[1:]

        # Checking to see if path was already registered
        if path in class_in_route:
            raise ValueError(
                f"'{path}'was set more than once on the same controller")
        class_in_route[path] = {"func": func, "methods": mapped_methods}

    def _methods_path_register(self, methods: list[str] | None, func: ROUTED_METHOD) -> list[HTTPMethods]:
        """Takes the list given methods and returns a list of the HTTPMethods."""

        try:
            if methods:
                return [METHODS_MAPPING_STR[method.upper()] for method in methods]
        except KeyError:
            raise ValueError(
                f"invalid values found in methods for '{func.__qualname__}'")
        # in case the methods aren't provided in the decorator but is instead
        # implied in the name of the method
        try:
            return [METHODS_MAPPING_STR[func.__name__.upper()]]
        except KeyError:
            raise ValueError(
                f"'{func.__qualname__}' must provide methods or must have the same name as an HTTP method")

    def _route_request(self, request: Request) -> Response:
        """Routes the request to the correct controller and method."""

        try:
            parsed_url = parse_url(request.url)
            controller = self._controllers[parsed_url.controller_path]
            method = self._get_method(
                controller, parsed_url.path, request.method)
            resp = Response(request.http_version)
            method(controller, request, resp)
            return resp
        except KeyError:
            return default_responses.NotFound(request.http_version)
        except MethodNotImplemented:
            return default_responses.MethodNotAllowed(request.http_version)
        except Exception as e:
            logging.exception(e)
            return default_responses.InternalServerError(request.http_version)

    def _get_method(self, controller: BaseController, path: str, method: HTTPMethods):

        controller_name = controller.__class__.__name__.lower()
        paths = self._routes[controller_name][path]

        # Check if method is supported
        if method in paths["methods"]:
            return paths["func"]
        raise MethodNotImplemented(method.value)

    def _send_response(self, resp: Response, conn: socket):

        deserialized_resp = HTTPParser.serialize_response(resp)
        resp_msg = SocketMessage(conn, ("", 0), deserialized_resp)
        Server.send_message(resp_msg)

    @staticmethod
    def _get_class_name(func: ROUTED_METHOD) -> str:
        """Gets the class name that the given method is defined under."""

        # Getting the class name and the method name
        names = func.__qualname__.split(".")
        # Not a method bound to a class
        # DOUBT: Is there a better way to do this?
        if len(names) != 2:
            raise TypeError(
                f"route decorator should be used only on methods of a class")
        return names[0].lower()


"""
1. Parse the request
2. Parse the url to get the controller
3. 
"""
