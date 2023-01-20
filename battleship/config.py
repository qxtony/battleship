from typing import Any, Final

from battleship.sockets import Server


class Config:
    def __init__(self):
        self.FPS: Final = 60
        self.WIDTH: Final = 1000
        self.HEIGHT: Final = 700
        self.TITLE: Final = "BattleShip"

        self.START_FIELD_COORDINATES: Final = 55, 220
        self.START_ENEMY_FIELD_COORDINATES: Final = 520, 220

        self.CELL_SIZE: Final = 40
        self.DISTANCE_CELLS: Final = 2
        self.MAX_CELLS_IN_LINE: Final = 10

        self.FIELD_BORDER_COLOR: Final = 48, 56, 65  # RGB
        self.SHIP_COLOR: Final = 200, 107, 133  # RGB
        self.DELIVERED_SHIP_COLOR: Final = 8, 105, 114  # RGB
        self.DEFAULT_SHIP_TYPE: Final = 4

        self.COLOR_INACTIVE_BOX = (141, 182, 205)  # RGB
        self.COLOR_ACTIVE_BOX = (28, 134, 238)  # RGB

        self.PRESSED_BUTTON_COLOR = (58, 71, 80)  # RGB
        self.UNPRESSED_BUTTON_COLOR = (240, 245, 249)  # RGB

        self.TEXT_COLOR = (255, 255, 255)  # RGB
        self.PICKER_COLOR = (61, 132, 168)  # RGB

        self.WHITE_COLOR: Final = (156, 167, 173)  # RGB
        self.GREEN_COLOR: Final = (23, 185, 120)  # RGB
        self.BLUE_COLOR: Final = (44, 133, 143)  # RGB

    def set_property(self, property_name: str, value: int) -> None:
        setattr(self, property_name, value)

    def get_property(self, property_name: str) -> Any:
        return getattr(self, property_name)


CONFIG = Config()
server = Server()
