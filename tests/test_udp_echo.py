import socket

import pytest

from echo.udp_client import udp_echo


@pytest.mark.parametrize(
    "message",
    [b"hello", b"", b"y" * 60_000, "Hey".encode()],
    ids=["short", "empty", "large-datagram", "hebrew-utf8"],
)
def test_echo_returns_same_bytes(udp_server, message):
    assert udp_echo(message, udp_server.address) == message


def test_message_boundaries_are_preserved(udp_server):
    # TCP is a stream and could merge these; UDP keeps each send as its own message
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(1)
        sock.sendto(b"one", udp_server.address)
        sock.sendto(b"two", udp_server.address)
        assert sock.recvfrom(65535)[0] == b"one"
        assert sock.recvfrom(65535)[0] == b"two"


def test_datagram_too_big_is_rejected(udp_server):
    # Max UDP payload over IPv4 is 65,507 bytes
    with pytest.raises(OSError):
        udp_echo(b"z" * 70_000, udp_server.address)


def test_no_reply_when_nothing_listens(unused_port):
    # Sending succeeds (UDP doesn't check), but no reply ever comes.
    # Linux times out; Windows reports the ICMP "port unreachable" as ConnectionResetError.
    with pytest.raises((TimeoutError, ConnectionResetError)):
        udp_echo(b"hi", ("127.0.0.1", unused_port), timeout=0.5)