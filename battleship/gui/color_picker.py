from typing import Optional, Tuple

import pygame

from battleship.config import CONFIG


class ColorPicker:
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.background = pygame.Surface((width, height))
        self.background.set_alpha(128)

        self.radius: int = height // 2
        self.column_width: int = width - height
        self.mouse_pressed: bool = False

        self.circle_position = 0
        self.color_limit = 360

        saturation = 50
        chroma = 30
        rect_height = 10

        self.filters = (saturation, chroma, rect_height)

        for i in range(self.column_width):
            color = pygame.Color(0)

            color.hsla = (
                self.color_limit * i / self.column_width,
                *self.filters,
            )

            pygame.draw.rect(
                self.background, color, (i, height // 3, i, rect_height)
            )

    def get_color(self) -> pygame.Color:
        color = pygame.Color(0)

        if self.circle_position * self.column_width > self.color_limit:
            color.hsla = (self.color_limit, *self.filters)

        else:
            color.hsla = (
                self.circle_position * self.column_width,
                *self.filters,
            )

        return color

    def update(self) -> Optional[pygame.Color]:
        mouse_pos: Tuple[int, int] = pygame.mouse.get_pos()
        mouse_buttons: Tuple[int, int, int] = pygame.mouse.get_pressed()

        if mouse_buttons[0]:
            self.mouse_pressed = True

        else:
            self.mouse_pressed = False

        if self.rect.collidepoint(mouse_pos) and self.mouse_pressed:
            self.circle_position: float = (
                mouse_pos[0] - self.rect.left - self.radius
            ) / self.column_width
            self.circle_position: int = max(0, min(self.circle_position, 1))

            return self.get_color()

    def draw(
        self,
        surface: pygame.Surface,
        indent_x: int = 5,
        indent_y: int = 5,
        thickness: int = 1,
        rounding: int = 5,
    ) -> None:
        surface.blit(self.background, self.rect)

        center: Tuple[int, int] = (
            self.rect.left
            + self.radius
            + self.circle_position * self.column_width,
            self.rect.centery,
        )
        pygame.draw.circle(
            surface, self.get_color(), center, self.rect.height // 2
        )

        rect_with_margins = (
            self.rect.x - indent_x / 2,
            self.rect.y - indent_y / 2,
            self.rect.width + indent_x,
            self.rect.height + indent_y,
        )
        pygame.draw.rect(
            surface,
            CONFIG.PICKER_COLOR,
            rect_with_margins,
            thickness,
            rounding,
        )
