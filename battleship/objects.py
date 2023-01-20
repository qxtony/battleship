from typing import Dict, Final, List

import pygame

from battleship.config import CONFIG
from battleship.elements import get_center_coordinates
from battleship.gui import Button, ColorPicker, InputBox
from battleship.resources.load import Screen
from battleship.sockets import data


class StartMenu:
    def __init__(self) -> None:
        self.font = pygame.font.Font(None, 64)
        settings = Screen.SETTINGS
        indent_settings: int = 10

        self.title = self.font.render("МОРСКОЙ БОЙ", True, CONFIG.TEXT_COLOR)
        start = self.font.render("Начать игру", True, CONFIG.TEXT_COLOR)
        server = self.font.render("Открыть сервер", True, CONFIG.TEXT_COLOR)

        self.start_game = Button(*get_center_coordinates(start), start)
        self.open_server = Button(*get_center_coordinates(server, 1), server)
        self.open_settings = Button(
            CONFIG.WIDTH - settings.get_width() - indent_settings,
            0,
            settings,
            draw_border=False,
        )

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.title, get_center_coordinates(self.title, -1))
        self.start_game.draw(screen)
        self.open_server.draw(screen)
        self.open_settings.draw(screen)

    def get_buttons(self) -> List[Button]:
        return [self.start_game, self.open_server, self.open_settings]


class SettingsMenu:
    def __init__(self, font_size: int = 35) -> None:
        self.font = pygame.font.Font(None, font_size)
        self.X_MARGIN_FROM_EDGE: Final = 450
        self.Y_MARGIN_FROM_EDGE: Final = 55
        self.DISTANCE_COLOR_PICKER: Final = 20
        self.INDENT_FROM_EDGE: Final = 10

        self.texts = {
            "CELL_SIZE": ("Размеры клетки:", False),
            "MAX_CELLS_IN_LINE": ("Количество клеток в ряду:", False),
            "FIELD_BORDER_COLOR": ("Цвет границы поля:", True),
            "SHIP_COLOR": ("Цвет корабля:", True),
            "DELIVERED_SHIP_COLOR": ("Цвет поставленного корабля:", True),
        }

        self.rendered_texts = [
            (self.font.render(text, True, CONFIG.TEXT_COLOR), is_color_picker)
            for text, is_color_picker in self.texts.values()
        ]

        self.input_boxes = []

        for position, (text, is_color_picker) in enumerate(
            self.rendered_texts
        ):
            if is_color_picker:
                box = ColorPicker(
                    self.X_MARGIN_FROM_EDGE,
                    (self.Y_MARGIN_FROM_EDGE * position)
                    - self.INDENT_FROM_EDGE,
                    self.X_MARGIN_FROM_EDGE,
                    self.Y_MARGIN_FROM_EDGE - self.DISTANCE_COLOR_PICKER,
                )

            else:
                box = InputBox(
                    self.X_MARGIN_FROM_EDGE,
                    self.Y_MARGIN_FROM_EDGE * position,
                    height=text.get_height(),
                )

            self.input_boxes.append(box)

        self.back = Button(
            CONFIG.WIDTH - Screen.BACK.get_width() - self.INDENT_FROM_EDGE,
            0,
            Screen.BACK,
            draw_border=False,
        )

    def draw(self, screen: pygame.Surface) -> None:
        for counter, (text, _) in enumerate(self.rendered_texts):
            screen.blit(
                text,
                (self.INDENT_FROM_EDGE, self.Y_MARGIN_FROM_EDGE * counter),
            )

        for input_box in self.input_boxes:
            input_box.draw(screen)

        self.back.draw(screen)

    def check_events(self, event) -> Dict[str, str]:
        data: Dict[str, str] = {}

        for property_name, box in zip(self.texts, self.input_boxes):
            if isinstance(box, ColorPicker):
                changed = box.update()

            else:
                changed = box.check_events(event)

            if changed:
                data[property_name] = changed

        return data

    def update(self) -> None:
        for input_box in self.input_boxes:
            input_box.update()


class ServerMenu:
    def __init__(
        self,
        font_size: int = 32,
        x: int = 5,
        y: int = 100,
        height: int = 90,
    ) -> None:
        self.y: int = y
        self.indent: int = 10
        self.height: int = height

        self.font = pygame.font.Font(None, font_size)
        self.frame = pygame.Rect(
            x, self.y, CONFIG.WIDTH - self.indent, self.height
        )

        self.title = self.font.render("Лобби", True, CONFIG.TEXT_COLOR)
        self.ip = self.font.render("IP Address", True, CONFIG.TEXT_COLOR)
        self.local_ip = self.font.render(
            f"Локальный IP: {data.SERVER_IP}", True, CONFIG.TEXT_COLOR
        )
        self.status = self.font.render("Статус", True, CONFIG.TEXT_COLOR)

        self.connected = self.font.render(
            "Подключен", True, CONFIG.GREEN_COLOR
        )

        self.back = Button(
            CONFIG.WIDTH - Screen.BACK.get_width() - self.indent,
            0,
            Screen.BACK,
            draw_border=False,
        )

        self.users: List[pygame.Surface] = []

    def draw(
        self,
        screen: pygame.Surface,
        thickness: int = 1,
        rounding: int = 5,
    ) -> None:
        pygame.draw.rect(
            screen, CONFIG.WHITE_COLOR, self.frame, thickness, rounding
        )
        pygame.draw.line(
            screen,
            CONFIG.TEXT_COLOR,
            (CONFIG.WIDTH / 2 - self.indent, self.y),
            (CONFIG.WIDTH / 2 - self.indent, self.height + self.y - 1),
        )

        screen.blit(self.title, get_center_coordinates(self.title, -4))
        screen.blit(
            self.local_ip,
            (
                CONFIG.WIDTH - self.local_ip.get_width() - self.indent,
                CONFIG.HEIGHT - self.local_ip.get_height() - self.indent,
            ),
        )

        screen.blit(self.ip, (self.indent, self.y))
        screen.blit(
            self.status,
            (CONFIG.WIDTH - self.status.get_width() - self.indent, self.y),
        )

        pygame.draw.line(
            screen,
            CONFIG.TEXT_COLOR,
            (
                self.indent - self.indent // 2,
                self.y + self.title.get_height() + self.indent // 2,
            ),
            (
                CONFIG.WIDTH - self.indent + self.indent // 2 - 1,
                self.y + self.title.get_height() + self.indent // 2,
            ),
        )

        for counter, user in enumerate(self.users):
            coordinates = (
                self.indent,
                self.y
                + self.title.get_height()
                + self.indent
                + counter * user.get_height(),
            )
            coordinates_connect = (
                CONFIG.WIDTH - self.connected.get_width() - self.indent,
                self.y
                + self.title.get_height()
                + self.indent
                + counter * user.get_height(),
            )

            screen.blit(user, coordinates)
            screen.blit(self.connected, coordinates_connect)

        self.back.draw(screen)

    def add_user(self, local_ip: str) -> None:
        self.users.append(self.font.render(local_ip, True, CONFIG.BLUE_COLOR))


class GetServerIPMenu:
    def __init__(self, font_size: int = 32) -> None:
        self.font = pygame.font.Font(None, font_size)
        indent: int = 40

        self.title = self.font.render(
            "Введите IP-адрес сервера:", True, CONFIG.TEXT_COLOR
        )
        x, y = get_center_coordinates(self.title)
        self.get_ip = InputBox(
            x + indent,
            y - 3,
            height=self.title.get_height(),
        )

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.title, get_center_coordinates(self.title, -1))
        self.get_ip.draw(screen)

    def get(self, event) -> str:
        return self.get_ip.check_events(event)

    def update(self):
        self.get_ip.update()


def draw_message(screen: pygame.Surface, text: str):
    font: pygame.font.Font = pygame.font.Font(None, 35)
    text = font.render(text, True, CONFIG.WHITE_COLOR)
    screen.blit(text, (250, 175))
