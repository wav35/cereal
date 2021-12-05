from typing import Tuple
from socketserver import BaseRequestHandler, TCPServer, ThreadingMixIn
from threading import Thread
from common import Cereal

class ServerHandler(BaseRequestHandler):
    """
    The handler to respond to requests
    """

    def handle(self):
        print('cl')
        while True:
            print('lp')
            data = self.request.recv(1024).strip().decode("ascii")
            self.server._handle_payload(self, data)

class CerealServer(Cereal, ThreadingMixIn, TCPServer):
    """
    Represents a host for a Cereal session.
    There is a single server and many clients
    """

    def __init__(self):
        super().__init__("server")
        TCPServer.__init__(self, ("0.0.0.0", 0), ServerHandler)
        self.thread = None
        self.clients = [] # Information of connected clients. See _handle_payload

    def _handle_payload(self, handler: BaseRequestHandler, payload: str):
        """
        Called by the handler.
        """
        resp = ""
        parts = payload.split("~")
        print(parts)
        opcode = parts[0]
        if opcode == "JOIN":
            self.clients.append({
                "handler": handler,
                "width": int(parts[1]), # Width of client's terminal, in characters
            })
            # Calculate the offset value for the client
            offset = 0
            for sock in self.clients:
                offset += sock["width"]
            resp = "JND~" + str(offset)
        b = bytearray()
        b.extend((resp + "\n").encode())
        handler.request.sendall(b)

    def send_content(self, content: str):
        payload = "CNT~" + content
        b = bytearray()
        b.extend((payload + "\n").encode())

        for cl in self.clients:
            cl["handler"].request.sendall(b)

    def display_marquee(self):
        payload = "DISP"
        b = bytearray()
        b.extend((payload + "\n").encode())
        for cl in self.clients:
            cl["handler"].request.sendall(b)

    def start_server(self) -> Tuple[str, int]:
        # Run the server in a background thread
        self.thread = Thread(target=super().serve_forever, daemon=True)
        self.thread.start()
        return self.socket.getsockname()

