from typing import Dict, Tuple

from pyglet import shapes

from ..config import CELL_WIDTH, CELL_HEIGHT, FIELD_BORDER_COLOR, SHIP_COLOR, DISTANCE_CELLS


def create_field_from_squares(
    x: int, y: int,
) -> Dict[shapes.BorderedRectangle, Tuple[int, int]]:
    field = {}
    for vertical in range(10):
        for horizontal in range(10):
            x_ship = x + vertical * (CELL_WIDTH + DISTANCE_CELLS)
            y_ship = y + horizontal * (CELL_HEIGHT + DISTANCE_CELLS)

            square = shapes.BorderedRectangle(
                x_ship, y_ship,
                width=CELL_WIDTH,
                height=CELL_HEIGHT,
                border_color=FIELD_BORDER_COLOR,
                border=2,
            )
            field[square] = (x_ship, y_ship)

    return field


def create_ship(
    x: int, y: int,
    ship_size: int,
    orientation: str = "horizontally",
) -> list[shapes.BorderedRectangle]:
    ships: list = []

    for ship in range(ship_size):
        if orientation == "horizontally":
            ship_x = x + ship * (CELL_WIDTH + DISTANCE_CELLS)
            ship_y = y
        else:
            ship_x = x
            ship_y = y + ship * (CELL_HEIGHT + DISTANCE_CELLS)

        ship = shapes.BorderedRectangle(
            ship_x, ship_y,
            width=CELL_WIDTH,
            height=CELL_HEIGHT,
            border_color=FIELD_BORDER_COLOR,
            border=2,
            color=SHIP_COLOR,
        )
        ships.append(ship)

    return ships
