import socket

import pytest

from echo.tcp_server import TCPEchoServer
from echo.udp_server import UDPEchoServer


@pytest.fixture
def tcp_server():
    server = TCPEchoServer()
    server.start()
    yield server
    server.stop()


@pytest.fixture
def udp_server():
    server = UDPEchoServer()
    server.start()
    yield server
    server.stop()


@pytest.fixture
def unused_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]