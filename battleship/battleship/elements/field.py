from typing import Dict

from .draw import create_field_from_squares


class Field:
    def __init__(self, start_x: int, start_y: int) -> None:
        self.field = create_field_from_squares(start_x, start_y)
        self.maximum_ships_counts: Dict[int, int] = {
            4: 1,
            3: 2,
            2: 3,
            1: 4,
        }

    def draw(self) -> None:
        for cell in self.field:
            cell.draw()
