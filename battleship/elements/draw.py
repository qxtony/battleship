from typing import List, Tuple

from pygame import Rect, Surface

from battleship.config import CONFIG
from battleship.resources.load import Screen

from .coordinates import get_cell_coordinates


def draw_background(screen: Surface) -> None:
    for x in range(CONFIG.WIDTH // Screen.EFFECT.get_width() + 1):
        for y in range(CONFIG.HEIGHT // Screen.EFFECT.get_height() + 1):
            screen.blit(
                Screen.EFFECT,
                (
                    x * Screen.EFFECT.get_width(),
                    y * Screen.EFFECT.get_height(),
                ),
            )


def draw_field_from_squares(
    x: int,
    y: int,
    field_thickness: int = 1,
) -> List[Tuple[Rect, tuple, int]]:
    field = []
    for vertical in range(CONFIG.MAX_CELLS_IN_LINE):
        for horizontal in range(CONFIG.MAX_CELLS_IN_LINE):
            x_ship = x + vertical * (CONFIG.CELL_SIZE + CONFIG.DISTANCE_CELLS)
            y_ship = y + horizontal * (
                CONFIG.CELL_SIZE + CONFIG.DISTANCE_CELLS
            )

            square = Rect(x_ship, y_ship, CONFIG.CELL_SIZE, CONFIG.CELL_SIZE)
            field.append((square, CONFIG.FIELD_BORDER_COLOR, field_thickness))

    return field


def draw_ship(
    x: int,
    y: int,
    ship_size: int,
    orientation: str = "horizontally",
    ship_thickness: int = 0,
) -> List[Tuple[Rect, int]]:
    ships: List[Tuple[Rect, int]] = []

    for size in range(ship_size):
        cell_x, cell_y = get_cell_coordinates(orientation, x, y, size)

        square = Rect(cell_x, cell_y, CONFIG.CELL_SIZE, CONFIG.CELL_SIZE)
        ships.append((square, ship_thickness))

    return ships
