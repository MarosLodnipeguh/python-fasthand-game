from enum import Enum


class EventName(Enum):
    """
    Enum class for event names. Used to store names of events in the game.
    """
    CHOOSE_CARD = 1
    PUT_CARD = 2
    DRAW_CARD = 3
    RESHUFFLE = 4