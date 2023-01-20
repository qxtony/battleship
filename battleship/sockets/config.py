import socket
from typing import Final


class Config:
    def __init__(self) -> None:
        self.LOCAL_IP: Final = "0.0.0.0"
        self.SERVER_IP = self.get_ip_address()
        self.PORT: Final = 35023
    
    def get_ip_address(self) -> str:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]


data = Config()
