from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from pygame import Rect, Surface, draw

from battleship.config import CONFIG
from battleship.elements.draw import draw_ship


class Ship:
    def __init__(
        self,
        x: int,
        y: int,
        size: int,
        ships_counter: Dict[int, int],
    ) -> None:
        self.x = x
        self.y = y
        self.health = size

        self.ships: List[Tuple[Rect, int]] = draw_ship(x, y, size)
        self.ships_counter: Dict[int, int] = ships_counter
        self.ships_counter[size] -= 1

        self.end_ship: bool = False
        self.color = CONFIG.SHIP_COLOR

        self.size: int = size
        self.orientation: str = "horizontally"

    def draw(self, screen: Surface) -> None:
        for ship, thickness in self.ships:
            draw.rect(screen, self.color, ship, thickness)

    def up(self, check: bool = True) -> None:
        self.move(0, CONFIG.CELL_SIZE + CONFIG.DISTANCE_CELLS)

        if check:
            self.check_for_going_over_edges()

    def down(self, check: bool = True) -> None:
        self.move(0, -(CONFIG.CELL_SIZE + CONFIG.DISTANCE_CELLS))

        if check:
            self.check_for_going_over_edges()

    def left(self, check: bool = True) -> None:
        self.move(-(CONFIG.CELL_SIZE + CONFIG.DISTANCE_CELLS), 0)

        if check:
            self.check_for_going_over_edges()

    def right(self, check: bool = True) -> None:
        self.move(CONFIG.CELL_SIZE + CONFIG.DISTANCE_CELLS, 0)

        if check:
            self.check_for_going_over_edges()

    def move(self, x: int, y: int) -> None:
        for ship in self.ships:
            ship[0][0] += x
            ship[0][1] += y

    def get_coordinates(self) -> tuple[int, int]:
        x: int = (self.ships[0][0][0] - self.x) // (
            CONFIG.CELL_SIZE + CONFIG.DISTANCE_CELLS
        ) + 1
        y: int = (self.ships[0][0][1] - self.y) // (
            CONFIG.CELL_SIZE + CONFIG.DISTANCE_CELLS
        ) + 1
        return x, y

    def check_for_going_over_edges(self) -> None:
        cell_x, cell_y = self.get_coordinates()

        if self.orientation == "horizontally":
            if cell_x + self.size > CONFIG.MAX_CELLS_IN_LINE + 1:
                self.left(check=False)

        elif self.orientation == "vertically":
            if cell_y + self.size < 0:
                self.up(check=False)

            elif cell_y + self.size > CONFIG.MAX_CELLS_IN_LINE + 1:
                self.down(check=False)

        if cell_y < 1:
            self.up(check=False)

        elif cell_x < 1:
            self.right(check=False)

        if cell_x > CONFIG.MAX_CELLS_IN_LINE:
            self.left(check=False)

        elif cell_y > CONFIG.MAX_CELLS_IN_LINE:
            self.down(check=False)

    def rotate(self) -> None:
        if self.orientation == "horizontally":
            self.orientation = "vertically"

        elif self.orientation == "vertically":
            self.orientation = "horizontally"

        self.recreate_ships()

    def check_ships_contact(self, ships: list[Ship]) -> bool:
        if len(ships) == 1:
            return False

        ships: list[Ship] = ships.copy()[:-1]

        for ship in ships:
            for ship_cell in ship.ships:
                for current_ship_cell in self.ships:
                    if (
                        current_ship_cell[0][0] == ship_cell[0][0]
                        and current_ship_cell[0][1] == ship_cell[0][1]
                    ):
                        return True

                    elif (
                        current_ship_cell[0][0] == ship_cell[0][0]
                        and current_ship_cell[0][1]
                        == ship_cell[0][1]
                        + CONFIG.CELL_SIZE
                        + CONFIG.DISTANCE_CELLS
                    ):
                        return True

                    elif (
                        current_ship_cell[0][0] == ship_cell[0][0]
                        and current_ship_cell[0][1]
                        == ship_cell[0][1]
                        - CONFIG.CELL_SIZE
                        - CONFIG.DISTANCE_CELLS
                    ):
                        return True

                    elif (
                        current_ship_cell[0][0]
                        == ship_cell[0][0]
                        + CONFIG.CELL_SIZE
                        + CONFIG.DISTANCE_CELLS
                        and current_ship_cell[0][1] == ship_cell[0][1]
                    ):
                        return True

                    elif (
                        current_ship_cell[0][0]
                        == ship_cell[0][0]
                        - CONFIG.CELL_SIZE
                        - CONFIG.DISTANCE_CELLS
                        and current_ship_cell[0][1] == ship_cell[0][1]
                    ):
                        return True

                    elif (
                        current_ship_cell[0][0]
                        == ship_cell[0][0]
                        + CONFIG.CELL_SIZE
                        + CONFIG.DISTANCE_CELLS
                        and current_ship_cell[0][1]
                        == ship_cell[0][1]
                        + CONFIG.CELL_SIZE
                        + CONFIG.DISTANCE_CELLS
                    ):
                        return True

                    elif (
                        current_ship_cell[0][0]
                        == ship_cell[0][0]
                        - CONFIG.CELL_SIZE
                        - CONFIG.DISTANCE_CELLS
                        and current_ship_cell[0][1]
                        == ship_cell[0][1]
                        + CONFIG.CELL_SIZE
                        + CONFIG.DISTANCE_CELLS
                    ):
                        return True

                    elif (
                        current_ship_cell[0][0]
                        == ship_cell[0][0]
                        + CONFIG.CELL_SIZE
                        + CONFIG.DISTANCE_CELLS
                        and current_ship_cell[0][1]
                        == ship_cell[0][1]
                        - CONFIG.CELL_SIZE
                        - CONFIG.DISTANCE_CELLS
                    ):
                        return True

                    elif (
                        current_ship_cell[0][0]
                        == ship_cell[0][0]
                        - CONFIG.CELL_SIZE
                        - CONFIG.DISTANCE_CELLS
                        and current_ship_cell[0][1]
                        == ship_cell[0][1]
                        - CONFIG.CELL_SIZE
                        - CONFIG.DISTANCE_CELLS
                    ):
                        return True

        return False

    def get_equal_zero(self) -> bool:
        return any(self.ships_counter.values())

    def get_next_ship(self, ships: list[Ship]) -> Optional[Ship]:
        for ship_size in self.ships_counter:
            if self.ships_counter[ship_size] > 0:
                new_ship = Ship(
                    self.x, self.y, ship_size, self.ships_counter.copy()
                )

                if not self.check_ships_contact(ships):
                    return new_ship

    def recreate_ships(self) -> None:
        self.ships: List[Tuple[Rect, int]] = draw_ship(
            self.ships[0][0][0],
            self.ships[0][0][1],
            ship_size=self.size,
            orientation=self.orientation,
        )
        for _ in range(self.size):
            self.check_for_going_over_edges()
