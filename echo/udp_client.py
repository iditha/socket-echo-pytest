import socket


def udp_echo(message: bytes, address, timeout=1.0) -> bytes:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(timeout)  # UDP never says "nobody's there", so don't wait forever
        sock.sendto(message, address)
        data, _ = sock.recvfrom(65535)  # one call = one whole datagram, no loop needed
        return data


if __name__ == "__main__":
    print(udp_echo(b"hello over UDP", ("127.0.0.1", 9001)))