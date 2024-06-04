class Card:
    """
    Card class that represents a card in the game. Created from the CardsEnum class entries.
    """
    name = "card name"
    full_name = "full card name"
    image_path = "image path"
    power = -1

    def __init__(self, name: str, full_name: str, image_path: str, power: int):
        """
        Constructor of the Card class
        :param name: short name of the card (e.g. 1H, 2D, 3C, 4S)
        :param full_name: full name of the card
        :param image_path: path to the image of the card
        :param power: power of the card (1-13) - used for comparing cards
        """
        self.name = name
        self.full_name = full_name
        self.image_path = image_path
        self.power = power

    def get_name(self):
        return self.name

    def get_full_name(self):
        return self.full_name

    def get_power(self):
        return self.power

    def get_image_path(self):
        return self.image_path
