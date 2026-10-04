import pytest

from echo.tcp_client import tcp_echo


@pytest.mark.parametrize(
    "message",
    [b"hello", b"", b"x" * 10_000, "שלום".encode()],
    ids=["short", "empty", "bigger-than-one-recv", "hebrew-utf8"],
)
def test_echo_returns_same_bytes(tcp_server, message):
    assert tcp_echo(message, tcp_server.address) == message


def test_server_handles_consecutive_clients(tcp_server):
    for i in range(5):
        msg = f"client {i}".encode()
        assert tcp_echo(msg, tcp_server.address) == msg


def test_connection_refused_when_nothing_listens(unused_port):
    with pytest.raises(ConnectionRefusedError):
        tcp_echo(b"hi", ("127.0.0.1", unused_port), timeout=5)