from typing import Final

from pygame import Surface, image, mixer

mixer.pre_init(44100, 32, 2, 4096)
mixer.init()


class Screen:
    EFFECT: Final[Surface] = image.load(
        "battleship/resources/images/effect.png"
    )
    BACKGROUND: Final[Surface] = image.load(
        "battleship/resources/images/background.png"
    )
    SETTINGS: Final[Surface] = image.load(
        "battleship/resources/images/settings.png"
    )
    BACK: Final[Surface] = image.load("battleship/resources/images/back.png")
    ICON_APPLICATION: Final[Surface] = image.load(
        "battleship/resources/images/icon.png"
    )
    BACKGROUND_MUSIC: Final[mixer.Sound] = mixer.Sound(
        "battleship/resources/sounds/background_music.wav"
    )
