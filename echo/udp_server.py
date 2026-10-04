import socket
import threading


class UDPEchoServer:
    """Receives UDP datagrams and sends each one back to its sender."""

    def __init__(self, host="127.0.0.1", port=0):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # DGRAM = UDP
        self._sock.bind((host, port))  # no listen(): UDP has no connections
        self._sock.settimeout(0.2)
        self.address = self._sock.getsockname()
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._serve, daemon=True)

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop.set()
        self._thread.join(timeout=2)
        self._sock.close()

    def _serve(self):
        while not self._stop.is_set():
            try:
                data, sender = self._sock.recvfrom(65535)  # one whole datagram + who sent it
            except socket.timeout:
                continue
            except ConnectionResetError:
                # Windows only: a previous reply hit a client that was already gone.
                # Ignore it, otherwise the server thread would crash.
                continue
            self._sock.sendto(data, sender)


if __name__ == "__main__":
    server = UDPEchoServer(port=9001)
    print(f"UDP echo server listening on {server.address}")
    server.start()
    input("Press Enter to stop\n")
    server.stop()