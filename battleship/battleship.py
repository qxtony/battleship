from typing import NoReturn

from pyglet import app, text, window

from config import *
from load_resources import ScreenResource, Ship
from utils import *


class Wordle(window.Window):  # type: ignore
    def __init__(self) -> None:
        super(Wordle, self).__init__(WIDTH, HEIGHT, TITLE)
        self.ships_coordinates: Dict[int, Tuple[int, int]] = {}
        self.ship_clamped_with_mouse = 0

        self.label = text.Label()

        self.set_icon(ScreenResource.icon_for_application)
        ScreenResource.background_music.play()

    def on_draw(self) -> NoReturn:
        self.clear()
        ScreenResource.background.blit(0, 0)

        print(self.ships_coordinates)

        for ship_number, (x, y) in self.ships_coordinates.items():
            self.label.draw()
            ship_picture_names: str = convert_ship_count_to_name(ship_number)
            Ship[ship_picture_names].value.blit(x, y)

    def on_mouse_press(self, x: int, y: int, button: int, _: int):
        if button not in MOUSE_KEYS:
            return False

        if ship_number := is_cursor_on_initial_ship_field(x, y):
            self.ship_clamped_with_mouse = ship_number

        elif ship_number := is_cursor_on_ship_field(
            x, y, self.ships_coordinates
        ):
            self.ship_clamped_with_mouse = ship_number

    def on_mouse_drag(self, x: int, y: int, *args) -> NoReturn:

        if self.ship_clamped_with_mouse:
            self.label = text.Label(
                f"{x}, {y}",
                font_name="Times New Roman",
                font_size=15,
                x=920,
                y=650,
                color=(0, 0, 0, 255),
            )
            self.ships_coordinates[self.ship_clamped_with_mouse] = (x, y)

    def on_mouse_release(self, x: int, y: int, *args):
        if not self.ship_clamped_with_mouse:
            return False

        if (
            x not in FieldProperties.X_FIELD_BORDERS
            or y not in FieldProperties.Y_FIELD_BORDERS
        ):
            self.ships_coordinates[
                self.ship_clamped_with_mouse
            ] = get_random_coordinates(
                self.ship_clamped_with_mouse, self.ships_coordinates
            )

        else:
            self.ships_coordinates[
                self.ship_clamped_with_mouse
            ] = get_coordinates_nearest_cell(x, y)
            for ship_size, coordination in self.ships_coordinates.items():
                self.ships_coordinates[ship_size] = is_ship_on_field(
                    *coordination, ship_size
                )


if __name__ == "__main__":
    window_game = Wordle()
    app.run()
