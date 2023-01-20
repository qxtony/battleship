import socket

from .config import data


class Server:
    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.users = []
        self.run = True
        self.allow = False

    def start(self) -> bool:
        self.socket.bind((data.LOCAL_IP, data.PORT))

        while self.run:
            message, user = self.socket.recvfrom(1024)

            if not self.allow:
                continue

            if user not in self.users:
                self.users.append(user)

            for client in self.users:
                if client != user:
                    self.socket.sendto(message, client)

    def allow_reception(self) -> None:
        self.allow = True
