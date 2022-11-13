import logging
import socket
from contextlib import contextmanager

from server.socket_request import SocketMessage

logger = logging.getLogger(__name__)


class Server:

    def __init__(self):

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def receive(self, hostname: str, port: int, tcp_connections_limit: int = 5):

        self._socket.bind((hostname, port))
        self._socket.listen(tcp_connections_limit)
        logger.warning(f"Socket ready to receive on port {port}")

    def get_message(self):

        logger.info("waiting for message")
        conn_socket, client_address = self._socket.accept()
        # DOUBT: Is the buffer size correct? How to determine buffer size?
        # Python guide shows how to do it using loop with fixed message length.
        # How to do it without a fixed message length?
        message = conn_socket.recv(1024)
        logger.info("received message")
        return SocketMessage(conn_socket, client_address, message)

    def close(self):

        self._socket.shutdown(1)
        self._socket.close()

    @staticmethod
    def send_message(socket_msg: SocketMessage):

        logger.debug("sending message")
        MSG_LEN = len(socket_msg.message)
        sent_bytes_len = 0
        while sent_bytes_len < MSG_LEN:
            sent_bytes = socket_msg.conn.send(socket_msg.message)
            sent_bytes_len += sent_bytes
        logger.debug("successfully sent message")
        logger.debug("closing connection")
        socket_msg.conn.close()
        logger.debug("closed connection")


@contextmanager
def make_server():

    server = Server()
    yield server
    logger.info("shutting down server")
    server.close()
