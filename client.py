import socket
from typing import Tuple
from utilities import string_to_figlet_array
from common import Cereal

class CerealClient(Cereal):
    def __init__(self, term_width: int):
        super().__init__("client")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.term_width = term_width

    def connect_to_addr(self, host: str, port: int) -> Tuple[list[list[int]], int]:
        """
        Connects to socket server and returns figlet array and relative offset
        """
        self.sock.connect((host, port))

        b = bytearray()
        b.extend(("JOIN~" + str(self.term_width) + "\n").encode())
        self.sock.sendall(b)

        fig_array = []
        rel_offset = 0

        while True:
            received = self.sock.recv(1024).strip().decode("ascii")
            parts = received.split("~")
            opcode = parts[0]

            print(parts)

            if opcode == "JND":
                rel_offset = int(parts[1])
            elif opcode == "CNT":
                fig_array = string_to_figlet_array(rel_offset, parts[1])
            elif opcode == "DISP":
                return (fig_array, rel_offset)

