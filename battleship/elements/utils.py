import pygame


def check_correct_number(number: str) -> bool:
    if isinstance(number, pygame.Color):
        return True

    if not number.isdigit():
        return False

    elif number.isalpha():
        return False

    return True
