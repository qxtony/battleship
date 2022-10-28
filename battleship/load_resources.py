from enum import Enum
from typing import Final

from pyglet import image, media


class ScreenResource:
    background: Final[image.AbstractImage] = image.load(
        "resources/images/background.png"
    )
    icon_for_application: Final[image.AbstractImage] = image.load(
        "resources/images/icon.png"
    )
    background_music: Final[media.Source] = media.load(
        "resources/sounds/background_music.mp3"
    )


class Ship(Enum):
    single_deck_ship: Final[image.AbstractImage] = image.load(
        "resources/images/ships/1.png"
    )
    two_deck_ship: Final[image.AbstractImage] = image.load(
        "resources/images/ships/2.png"
    )
    three_deck_ship: Final[image.AbstractImage] = image.load(
        "resources/images/ships/3.png"
    )
    four_deck_ship: Final[image.AbstractImage] = image.load(
        "resources/images/ships/4.png"
    )
