from typing import Final

from pyglet import image, media


class Screen:
    background: Final[image.AbstractImage] = image.load(
        "battleship/resources/images/background.png"
    )
    icon_application: Final[image.AbstractImage] = image.load(
        "battleship/resources/images/icon.png"
    )
    background_music: Final[media.Source] = media.load(
        "battleship/resources/sounds/background_music.mp3"
    )
