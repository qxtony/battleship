from pygame import Rect, Surface, draw

from battleship.config import CONFIG
from battleship.elements.draw import draw_field_from_squares
from battleship.elements.ship import Ship


class Field:
    def __init__(self, start_x: int, start_y: int) -> None:
        self.start_x = start_x
        self.start_y = start_y

        self.field = draw_field_from_squares(start_x, start_y)

        self.ships_counter: dict[int, int] = {
            4: 1,
            3: 2,
            2: 3,
            1: 4,
        }
        self.ships: list[Ship] = [
            Ship(
                start_x, start_y, CONFIG.DEFAULT_SHIP_TYPE, self.ships_counter
            )
        ]
        self.field_dot = []
        self.field_cross = []
        self.dead_ships = []

    def draw_ships(self, screen: Surface) -> None:
        for ship in self.ships:
            ship.draw(screen)

        for x, y in self.field_dot:
            draw.circle(
                screen,
                CONFIG.SHIP_COLOR,
                (
                    self.start_x
                    + x * CONFIG.CELL_SIZE
                    + x * CONFIG.DISTANCE_CELLS
                    + CONFIG.CELL_SIZE // 2,
                    self.start_y
                    + y * CONFIG.CELL_SIZE
                    + y * CONFIG.DISTANCE_CELLS
                    + CONFIG.CELL_SIZE // 2,
                ),
                2,
            )

        for x, y in self.field_cross:
            x = self.start_x + x * CONFIG.CELL_SIZE + x * CONFIG.DISTANCE_CELLS
            y = self.start_y + y * CONFIG.CELL_SIZE + y * CONFIG.DISTANCE_CELLS

            draw.line(
                screen,
                CONFIG.SHIP_COLOR,
                (x, y),
                (x + CONFIG.CELL_SIZE - 1, y + CONFIG.CELL_SIZE - 1),
                2,
            )
            draw.line(
                screen,
                CONFIG.SHIP_COLOR,
                (x + CONFIG.CELL_SIZE - 1, y + 1),
                (x, y + CONFIG.CELL_SIZE - 1),
                2,
            )

        for x, y, size, orientation in self.dead_ships:
            x -= 1
            y -= 1

            if orientation == "horizontally":
                draw.rect(
                    screen,
                    CONFIG.SHIP_COLOR,
                    (
                        self.start_x
                        + x * CONFIG.CELL_SIZE
                        + x * CONFIG.DISTANCE_CELLS,
                        self.start_y
                        + y * CONFIG.CELL_SIZE
                        + y * CONFIG.DISTANCE_CELLS,
                        CONFIG.CELL_SIZE * size
                        + CONFIG.DISTANCE_CELLS * (size - 1),
                        CONFIG.CELL_SIZE,
                    ),
                    1,
                )
            else:
                draw.rect(
                    screen,
                    CONFIG.SHIP_COLOR,
                    (
                        self.start_x
                        + x * CONFIG.CELL_SIZE
                        + x * CONFIG.DISTANCE_CELLS,
                        self.start_y
                        + y * CONFIG.CELL_SIZE
                        + y * CONFIG.DISTANCE_CELLS,
                        CONFIG.CELL_SIZE,
                        CONFIG.CELL_SIZE * size
                        + CONFIG.DISTANCE_CELLS * (size - 1),
                    ),
                    1,
                )

    def draw(self, screen: Surface) -> None:
        for cell, color, thickness in self.field:
            draw.rect(screen, color, cell, thickness)

    def append_new_ship(self) -> bool:
        selected_ship: Ship = self.ships[-1]
        next_ship: Ship = selected_ship.get_next_ship(self.ships.copy())

        if next_ship:
            self.ships.append(next_ship)
            selected_ship.color = CONFIG.DELIVERED_SHIP_COLOR

        if not selected_ship.get_equal_zero():
            selected_ship.color = CONFIG.DELIVERED_SHIP_COLOR
            selected_ship.end_ship = True

        return selected_ship.get_equal_zero()


class EnemyField:
    def __init__(self, start_x: int, start_y: int) -> None:
        self.start_x = start_x
        self.start_y = start_y

        self.field = draw_field_from_squares(start_x, start_y)

        self.ships_counter: dict[int, int] = {
            4: 1,
            3: 2,
            2: 3,
            1: 4,
        }
        self.attacks = []
        self.marks = []
        self.attacks.append(
            Rect(
                self.start_x, self.start_y, CONFIG.CELL_SIZE, CONFIG.CELL_SIZE
            )
        )
        self.marks.append("none")
        self.dead_ships = []

    def draw(self, screen: Surface) -> None:
        for cell, color, thickness in self.field:
            draw.rect(screen, color, cell, thickness)

    def draw_ships(self, screen: Surface) -> None:
        for position, (mark, cell) in enumerate(zip(self.marks, self.attacks)):
            previous_ship = self.attacks[position - 1]

            if mark == "cross":
                self.draw_cross(screen, previous_ship)

            elif mark == "dot":
                self.draw_dot(screen, previous_ship)

            if cell == self.attacks[-1]:
                draw.rect(screen, CONFIG.SHIP_COLOR, cell, 1)

            else:
                draw.rect(screen, CONFIG.DELIVERED_SHIP_COLOR, cell, 1)

        for x, y, size, orientation in self.dead_ships:
            x -= 1
            y -= 1

            if orientation:
                draw.rect(
                    screen,
                    CONFIG.DELIVERED_SHIP_COLOR,
                    (
                        self.start_x
                        + x * CONFIG.CELL_SIZE
                        + x * CONFIG.DISTANCE_CELLS,
                        self.start_y
                        + y * CONFIG.CELL_SIZE
                        + y * CONFIG.DISTANCE_CELLS,
                        CONFIG.CELL_SIZE * size
                        + CONFIG.DISTANCE_CELLS * (size - 1),
                        CONFIG.CELL_SIZE,
                    ),
                    1,
                )
            else:
                draw.rect(
                    screen,
                    CONFIG.DELIVERED_SHIP_COLOR,
                    (
                        self.start_x
                        + x * CONFIG.CELL_SIZE
                        + x * CONFIG.DISTANCE_CELLS,
                        self.start_y
                        + y * CONFIG.CELL_SIZE
                        + y * CONFIG.DISTANCE_CELLS,
                        CONFIG.CELL_SIZE,
                        CONFIG.CELL_SIZE * size
                        + CONFIG.DISTANCE_CELLS * (size - 1),
                    ),
                    1,
                )

    def up(self, check: bool = True) -> None:
        current_cell = self.attacks[-1]
        current_cell.y -= CONFIG.CELL_SIZE + CONFIG.DISTANCE_CELLS

        if check:
            self.check_for_going_over_edges()

    def down(self, check: bool = True) -> None:
        current_cell = self.attacks[-1]
        current_cell.y += CONFIG.CELL_SIZE + CONFIG.DISTANCE_CELLS

        if check:
            self.check_for_going_over_edges()

    def right(self, check: bool = True) -> None:
        current_cell = self.attacks[-1]
        current_cell.x += CONFIG.CELL_SIZE + CONFIG.DISTANCE_CELLS

        if check:
            self.check_for_going_over_edges()

    def left(self, check: bool = True) -> None:
        current_cell = self.attacks[-1]
        current_cell.x -= CONFIG.CELL_SIZE + CONFIG.DISTANCE_CELLS

        if check:
            self.check_for_going_over_edges()

    def apply(self, client) -> None:
        for cell in self.attacks:
            if cell not in self.attacks[:-1]:
                client.send_message(f"attack {self.get_coordinates()}")
                self.attacks.append(
                    Rect(cell.x, cell.y, CONFIG.CELL_SIZE, CONFIG.CELL_SIZE)
                )

    def get_coordinates(self) -> tuple[int, int]:
        x: int = (self.attacks[-1].x - self.start_x) // (
            CONFIG.CELL_SIZE + CONFIG.DISTANCE_CELLS
        )
        y: int = (self.attacks[-1].y - self.start_y) // (
            CONFIG.CELL_SIZE + CONFIG.DISTANCE_CELLS
        )
        return x, y

    def check_for_going_over_edges(self) -> None:
        cell_x, cell_y = self.get_coordinates()

        if cell_x > CONFIG.MAX_CELLS_IN_LINE - 1:
            self.left(check=False)

        elif cell_y > CONFIG.MAX_CELLS_IN_LINE - 1:
            self.up(check=False)

        if cell_y < 0:
            self.down(check=False)

        elif cell_x < 0:
            self.right(check=False)

    def draw_cross(self, screen: Surface, cell: Surface) -> None:
        draw.line(
            screen,
            CONFIG.DELIVERED_SHIP_COLOR,
            (cell.x, cell.y),
            (cell.x + CONFIG.CELL_SIZE - 1, cell.y + CONFIG.CELL_SIZE - 1),
            2,
        )

        draw.line(
            screen,
            CONFIG.DELIVERED_SHIP_COLOR,
            (cell.x + CONFIG.CELL_SIZE - 1, cell.y + 1),
            (cell.x + 1, cell.y + CONFIG.CELL_SIZE - 1),
            2,
        )

    def draw_dot(self, screen: Surface, cell: Surface) -> None:
        draw.circle(
            screen,
            CONFIG.SHIP_COLOR,
            (cell.x + CONFIG.CELL_SIZE // 2, cell.y + CONFIG.CELL_SIZE // 2),
            2,
        )
