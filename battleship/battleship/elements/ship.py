from typing import Final
from time import sleep

from pyglet import shapes

from .draw import create_ship
from ..config import CELL_WIDTH, CELL_HEIGHT, START_FIELD_COORDINATES, DISTANCE_CELLS


class Ship:
    def __init__(self, size: int = 4) -> None:
        self.ships: list[shapes.BorderedRectangle] = create_ship(
            *START_FIELD_COORDINATES, size
        )
        self.size = size
        self.max_cells_in_line: Final = 10
        self.orientation = "horizontally"

    def draw(self) -> None:
        for ship in self.ships:
            ship.draw()

    def up(self) -> None:
        self.move(0, CELL_HEIGHT + DISTANCE_CELLS)
        self.check_for_going_over_edges()

    def down(self) -> None:
        self.move(0, -(CELL_HEIGHT + DISTANCE_CELLS))
        self.check_for_going_over_edges()

    def left(self) -> None:
        self.move(-(CELL_WIDTH + DISTANCE_CELLS), 0)
        self.check_for_going_over_edges()

    def right(self) -> None:
        self.move(CELL_WIDTH + DISTANCE_CELLS, 0)
        self.check_for_going_over_edges()

    def move(self, x: int, y: int) -> None:
        for ship in self.ships:

            for _ in range(10):
                ship.x += x / 10
                sleep(0.001)

            ship.y += y

    def check_for_going_over_edges(self) -> None:
        cell_x, cell_y = self.get_coordinates()

        if self.orientation == "horizontally":
            if cell_x + self.size > self.max_cells_in_line + 1:
                self.left()

        elif self.orientation == "vertically":
            if cell_y + self.size < 0:
                self.up()

            elif cell_y + self.size > self.max_cells_in_line + 1:
                self.down()

        if cell_y < 1:
            self.up()

        elif cell_x < 1:
            self.right()

        if cell_x > self.max_cells_in_line:
            self.left()

        elif cell_y > self.max_cells_in_line:
            self.down()

    def switch_orientation(self) -> None:
        if self.orientation == "horizontally":
            self.orientation = "vertically"

        elif self.orientation == "vertically":
            self.orientation = "horizontally"

        self.recreate_ships()

    def recreate_ships(self) -> None:
        x, y = self.ships[0].x, self.ships[0].y

        self.ships: list[shapes.BorderedRectangle] = create_ship(
            x, y,
            self.size, self.orientation
        )
        self.check_for_going_over_edges()

    def get_coordinates(self) -> tuple[int, int]:
        x = self.ships[0].x // (CELL_WIDTH + DISTANCE_CELLS)
        y = self.ships[0].y // (CELL_HEIGHT + DISTANCE_CELLS)
        return x, y
