import socket

from shared.protocol import Command


class CommandListener:
    BUFFSIZE = 2 ** 16

    def __init__(self, server_addr: str):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(server_addr)

    def gen_command(self) -> Command:
        cmd_bytes, addr = self.sock.recvfrom(self.BUFFSIZE)
        msg = Command.from_bytes(cmd_bytes)
        yield msg
