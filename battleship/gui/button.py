from typing import Optional

from pygame import MOUSEBUTTONDOWN, Rect, Surface, draw, mouse

from battleship.config import CONFIG


class Button:
    def __init__(
        self,
        x: int,
        y: int,
        text: Surface,
        offset_x: int = 10,
        offset_y: int = 10,
        draw_border: bool = True,
    ) -> None:
        width: int = text.get_width() - offset_x
        height: int = text.get_height() + offset_y
        self.draw_border: bool = draw_border

        self.button = Rect(x, y, width, height)
        self.color = CONFIG.UNPRESSED_BUTTON_COLOR
        self.text = text

    def check_click(self, event) -> Optional[bool]:
        if event.type == MOUSEBUTTONDOWN and self.button.collidepoint(
            event.pos
        ):
            self.color = CONFIG.PRESSED_BUTTON_COLOR
            return True

        if self.button.collidepoint(mouse.get_pos()):
            self.color = CONFIG.PRESSED_BUTTON_COLOR

        else:
            self.color = CONFIG.UNPRESSED_BUTTON_COLOR

    def draw(
        self,
        screen: Surface,
        thickness: int = 1,
        offset_x: int = 5,
        offset_y: int = 5,
        rounding: int = 5,
        lengthening: int = 100,
    ) -> None:
        button = (
            self.button.x - lengthening / 2 + offset_x,
            self.button.y,
            self.button.width + lengthening,
            self.button.height,
        )
        if self.draw_border:
            draw.rect(screen, self.color, button, thickness, rounding)

        screen.blit(
            self.text, (self.button.x - offset_x, self.button.y + offset_y)
        )
