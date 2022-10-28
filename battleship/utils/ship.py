from typing import Final


class ShipProperties:
    SHIP_BORDER_Y: Final = range(35, 70)
    BORDERS_SINGLE_DECK_SHIP: Final = range(105, 140)
    BORDERS_TWO_DECK_SHIP: Final = range(335, 405)
    BORDERS_THREE_DECK_SHIP: Final = range(570, 670)
    BORDERS_FOUR_DECK_SHIP: Final = range(800, 935)

    SHIP_NAMES: Final = {
        1: "single_deck_ship",
        2: "two_deck_ship",
        3: "three_deck_ship",
        4: "four_deck_ship",
    }
