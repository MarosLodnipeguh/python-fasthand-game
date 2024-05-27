class Player:
    def __init__(self):
        self.hand = []
        self.supply = []
        self.reshuffle = []

    def draw_card(self):
        if self.supply and len(self.hand) < 5:
            self.hand.append(self.supply.pop())

    def play_card(self, card_index, gamestacks):
        card = self.hand[card_index]
        for stack in gamestacks:
            if stack.can_play(card):
                self.hand.pop(card_index)
                stack.add_card(card)
                return True
        return False
