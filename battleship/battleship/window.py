from typing import List

from pyglet import clock, window

from .resources.load import Screen
from .config import *
from .elements import Field, Ship


class BattleShip(window.Window):
    def __init__(self) -> None:
        super(BattleShip, self).__init__(WIDTH, HEIGHT, TITLE)
        self.set_icon(Screen.icon_application)

        self.field = Field(*START_FIELD_COORDINATES)
        self.enemy_field = Field(*START_ENEMY_FIELD_COORDINATES)

        self.ships: List[Ship] = [Ship()]
        self.field.maximum_ships_counts[4] -= 1

        self.play_background_music()
        clock.schedule_interval(self.play_background_music, MUSIC_DURATION)
        clock.schedule_interval(self.on_draw, 1 / 60)

    @staticmethod
    def play_background_music(_: int = None) -> None:
        Screen.background_music.play()

    def on_draw(self, _: int = None) -> None:
        self.clear()
        Screen.background.blit(0, 0)

        self.field.draw()
        self.enemy_field.draw()

        for ship in self.ships:
            ship.draw()

    def on_key_press(self, symbol: int, _: int) -> None:
        selected_ship = self.ships[-1]

        if symbol == window.key.ESCAPE:
            self.close()

        elif symbol == window.key.W:
            selected_ship.up()

        elif symbol == window.key.A:
            selected_ship.left()

        elif symbol == window.key.S:
            selected_ship.down()

        elif symbol == window.key.D:
            selected_ship.right()

        elif symbol == window.key.SPACE:
            selected_ship.switch_orientation()

        elif symbol == window.key.ENTER:
            for ship_size in self.field.maximum_ships_counts:
                if self.field.maximum_ships_counts[ship_size] > 0:
                    self.field.maximum_ships_counts[ship_size] -= 1
                    self.ships.append(Ship(ship_size))
                    break
