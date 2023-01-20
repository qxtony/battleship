from typing import Optional, Tuple

import pygame

from battleship.config import CONFIG


class InputBox:
    def __init__(
        self,
        x: int,
        y: int,
        width: int = 1,
        height: int = 1,
        font_size: int = 30,
    ) -> None:
        self.txt_surface: pygame.font = None

        self.rect: pygame.Rect = pygame.Rect(x, y, width, height)
        self.color: Tuple[int, int, int, int] = CONFIG.COLOR_INACTIVE_BOX
        self.collide: bool = False

        self.text: str = ""
        self.FONT: pygame.font.Font = pygame.font.Font(None, font_size)
        self.render_text()

    def render_text(self) -> None:
        self.txt_surface = self.FONT.render(self.text, True, self.color)

    def switch_color(self) -> None:
        if self.color == CONFIG.COLOR_ACTIVE_BOX:
            self.color = CONFIG.COLOR_INACTIVE_BOX
            self.collide = False

        else:
            self.color = CONFIG.COLOR_ACTIVE_BOX
            self.collide = True

    def check_click_on_rect(self, position: Tuple[int, int]) -> None:
        if self.rect.collidepoint(position):
            self.switch_color()

    def change_text(self, event: pygame.event.Event) -> Optional[str]:
        if event.key == pygame.K_RETURN:
            text: str = self.text
            self.text = ""
            self.switch_color()
            self.render_text()
            return text

        elif event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]

        else:
            self.text += event.unicode

        self.render_text()

    def check_events(self, event) -> Optional[str]:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.color = CONFIG.COLOR_ACTIVE_BOX
                self.collide = True

            else:
                self.color = CONFIG.COLOR_INACTIVE_BOX
                self.collide = False

        if event.type == pygame.KEYDOWN and self.collide:
            return self.change_text(event)

    def update(self, indent: int = 10) -> None:
        self.rect.width = max(200, self.txt_surface.get_width() + indent)

    def draw(
        self,
        screen: pygame.Surface,
        indent_x: int = 5,
        indent_y: int = 5,
        thickness: int = 2,
        rounding: int = 5,
    ) -> None:
        screen.blit(
            self.txt_surface, (self.rect.x + indent_x, self.rect.y + indent_y)
        )
        pygame.draw.rect(screen, self.color, self.rect, thickness, rounding)
