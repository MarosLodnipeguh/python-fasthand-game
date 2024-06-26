from enum import Enum


class GameState(Enum):
    """
    Enum class for game states. Used to store states of the game.
    """
    READY = 1
    GAME_IN_PROGRESS = 2
    WAITING_FOR_RESHUFFLE = 3
    PLAYER_1_WINS = 4
    PLAYER_2_WINS = 5
    GAME_DRAW = 6
