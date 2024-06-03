from enum import Enum


class EventName(Enum):
    CHOOSE_CARD = 1
    PUT_CARD = 2
    DRAW_CARD = 3
    RESHUFFLE = 4