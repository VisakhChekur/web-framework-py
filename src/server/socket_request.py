from socket import socket
from dataclasses import dataclass
from typing import Tuple


@dataclass
class SocketMessage:

    conn: socket
    client_address: Tuple[str, int]
    message: bytes
