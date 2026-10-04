import socket


def tcp_echo(message: bytes, address, timeout=2.0) -> bytes:
    with socket.create_connection(address, timeout=timeout) as sock:
        sock.sendall(message)
        sock.shutdown(socket.SHUT_WR)  # sends FIN: "I'm done sending"
        chunks = []
        while chunk := sock.recv(4096):  # TCP is a stream: read until the server closes
            chunks.append(chunk)
    return b"".join(chunks)


if (__name__ ==
        "__main__"):
    print(tcp_echo(b"hello over TCP", ("127.0.0.1", 9000)))