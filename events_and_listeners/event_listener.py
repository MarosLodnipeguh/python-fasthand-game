from abc import ABC, abstractmethod


class EventListener(ABC):
    # @abstractmethod
    # def notify(self, event):
    #     pass

    @abstractmethod
    def repaint(self):
        pass

    @abstractmethod
    def reshuffle_call(self):
        pass

    @abstractmethod
    def reshuffle_done(self):
        pass

    @abstractmethod
    def player_1_wins(self):
        pass

    @abstractmethod
    def player_2_wins(self):
        pass

    @abstractmethod
    def game_draw(self):
        pass

    def set_shared_lists(self, p1_hand, p1_supply, p1_reshuffle, p2_hand, p2_supply, p2_reshuffle, gamestack1,
                         gamestack2):
        pass

