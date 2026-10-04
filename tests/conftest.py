import socket

import pytest

from echo.tcp_server import TCPEchoServer


@pytest.fixture
def tcp_server():
    server = TCPEchoServer()
    server.start()
    yield server        # the test runs here
    server.stop()       # cleanup, even if the test failed


@pytest.fixture
def unused_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]