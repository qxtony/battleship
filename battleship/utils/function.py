from random import randint
from typing import Dict, Final, Optional, Tuple

from .field import FieldProperties
from .ship import ShipProperties


def get_ship_borders() -> Dict[range, int]:
    SHIP_NUMBERS: Final[Dict[range, int]] = {
        ShipProperties.BORDERS_SINGLE_DECK_SHIP: 1,
        ShipProperties.BORDERS_TWO_DECK_SHIP: 2,
        ShipProperties.BORDERS_THREE_DECK_SHIP: 3,
        ShipProperties.BORDERS_FOUR_DECK_SHIP: 4,
    }
    return SHIP_NUMBERS


def is_cursor_on_initial_ship_field(
        cursor_x: int, cursor_y: int
) -> Optional[int]:
    for border_x, ship_number in get_ship_borders().items():
        if cursor_x in border_x and cursor_y in ShipProperties.SHIP_BORDER_Y:
            return ship_number


def is_cursor_on_ship_field(
        x: int, y: int, ships_coordinates: Dict[int, Tuple[int, int]]
) -> Optional[int]:
    for ship_number, (x_ship, y_ship) in ships_coordinates.items():
        ship_size = FieldProperties.SIZE_OF_CELL

        x_border = range(x_ship, x_ship + ship_size * ship_number)
        y_border = range(y_ship, y_ship + ship_size)

        if x in x_border and y in y_border:
            return ship_number


def convert_ship_count_to_name(ship_shape: int) -> str:
    return ShipProperties.SHIP_NAMES[ship_shape]


def get_ship_coordinates(position_x: int, position_y: int) -> Tuple[int, int]:
    cell_size = FieldProperties.SIZE_OF_CELL

    x = FieldProperties.X_BEGINNING_FIELD + cell_size * position_x
    y = FieldProperties.Y_BEGINNING_FIELD - cell_size * position_y

    return x, y


def get_adjacent_ships(coordinates: Dict[int, Tuple[int, int]]):
    cell_size = FieldProperties.SIZE_OF_CELL


def get_random_coordinates(
        ship_size: int, coordinates: Dict[int, Tuple[int, int]]
) -> Tuple[int, int]:
    cell_size = FieldProperties.SIZE_OF_CELL
    DEFAULT_COORDINATES: Final = {0: (0, 0)}
    coord = coordinates.items() or DEFAULT_COORDINATES.items()

    for position_x in range(1, 10 - ship_size):
        for position_y in range(1, 9):
            x, y = get_ship_coordinates(position_x, position_y)

            if not (
                    x in range(x_ship, x_ship + cell_size * ship_number)
                    and x + cell_size * position_x in range(x_ship, x_ship + cell_size * ship_number)
                    and y in range(y_ship, y_ship + cell_size)
                    for ship_number, (x_ship, y_ship) in coord
            ):
                return is_ship_on_field(x, y, ship_size)


def take_away_remains(x: int, y: int) -> Tuple[int, int]:
    sell_size = FieldProperties.SIZE_OF_CELL

    remains_x = (x - FieldProperties.X_BEGINNING_FIELD) % sell_size
    remains_y = (FieldProperties.Y_BEGINNING_FIELD - y) % sell_size

    x -= remains_x * (1 if remains_x < 15 else -1)
    y += remains_y * (1 if remains_y < 15 else -1)

    return x, y


def get_rounded_cell_coordinates(x: int, y: int) -> Tuple[int, int]:
    x_beginning_field = FieldProperties.X_BEGINNING_FIELD
    y_beginning_field = FieldProperties.Y_BEGINNING_FIELD
    sell_size = FieldProperties.SIZE_OF_CELL

    x_cell = (x - x_beginning_field) // sell_size
    y_cell = (y_beginning_field - y) // sell_size

    x = x_beginning_field + sell_size * x_cell
    y = y_beginning_field - sell_size * y_cell

    return x, y


def get_coordinates_nearest_cell(
        cursor_x: int,
        cursor_y: int,
) -> Tuple[int, int]:
    coordinates = get_rounded_cell_coordinates(
        *take_away_remains(cursor_x, cursor_y)
    )
    return coordinates


def is_ship_on_field(x: int, y: int, ship_size: int) -> Tuple[int, int]:
    x_end_field = FieldProperties.X_END_FIELD

    cell_size = FieldProperties.SIZE_OF_CELL

    if x + cell_size * ship_size > x_end_field:
        x -= (x + cell_size * (ship_size - 1)) - x_end_field

    return x, y
