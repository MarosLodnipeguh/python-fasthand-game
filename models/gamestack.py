class GameStack:
    def __init__(self):
        self.stack = []

    def add_card(self, card):
        self.stack.append(card)

    def top_card(self):
        return self.stack[-1] if self.stack else None

    def can_play(self, card):
        top_card = self.top_card()
        if not top_card:
            return False
        top_power = top_card.get_power()
        card_power = card.get_power()
        return (card_power == top_power + 1 or card_power == top_power - 1 or
                (card_power == 1 and top_power == 13) or
                (card_power == 13 and top_power == 1))
