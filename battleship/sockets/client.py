import socket

from .config import data


class Client:
    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("", 0))
        self.send_message("Client started")

    def send_message(self, message: str) -> None:
        self.socket.sendto(
            message.encode("utf-8"), (data.SERVER_IP, data.PORT)
        )

    def accept_messages(self) -> str:
        try:
            return self.socket.recv(1024)

        except ConnectionResetError:
            return b""
