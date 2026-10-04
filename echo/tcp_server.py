import socket
import threading


class TCPEchoServer:
    """Accepts TCP connections and sends back every byte it receives."""

    def __init__(self, host="127.0.0.1", port=0):
        # port=0 asks the OS for any free port, so tests never collide
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((host, port))
        self._sock.listen()
        self._sock.settimeout(0.2)  # lets the loop check regularly whether to stop
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
                conn, _ = self._sock.accept()
            except socket.timeout:
                continue
            with conn:
                while data := conn.recv(4096):
                    conn.sendall(data)


if __name__ == "__main__":
    server = TCPEchoServer(port=9000)
    print(f"TCP echo server listening on {server.address}")
    server.start()
    input("Press Enter to stop\n")
    server.stop()