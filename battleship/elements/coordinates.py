from typing import Tuple

from pygame import Surface

from battleship.config import CONFIG


def get_center_coordinates(
    text: Surface,
    offset_count: int = 0,
    offset: int = 80,
) -> Tuple[int, int]:
    x = CONFIG.WIDTH // 2 - (text.get_width()) // 2
    y = (CONFIG.HEIGHT // 2 - (text.get_height()) // 2) + (
        offset_count * offset
    )

    return x, y


def get_cell_coordinates(
    ship_orientation: str,
    x: int,
    y: int,
    size: int,
) -> Tuple[int, int]:
    if ship_orientation == "horizontally":
        x += size * (CONFIG.CELL_SIZE + CONFIG.DISTANCE_CELLS)
    else:
        y += size * (CONFIG.CELL_SIZE + CONFIG.DISTANCE_CELLS)

    return x, y
