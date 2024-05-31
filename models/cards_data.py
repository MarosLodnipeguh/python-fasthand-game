# cards_data.py
from enum import Enum


class CardsEnum(Enum):
    def __init__(self, full_name, image_path, power):
        self.full_name = full_name
        self.image_path = image_path
        self.power = power

    # name : (full_name, image_path, power)

    # Hearts - Kier
    H1 = ("Ace of Hearts", "resources/images/1_of_hearts.png", 1)
    H2 = ("2 of Hearts", "resources/images/2_of_hearts.png", 2)
    H3 = ("3 of Hearts", "resources/images/3_of_hearts.png", 3)
    H4 = ("4 of Hearts", "resources/images/4_of_hearts.png", 4)
    H5 = ("5 of Hearts", "resources/images/5_of_hearts.png", 5)
    H6 = ("6 of Hearts", "resources/images/6_of_hearts.png", 6)
    H7 = ("7 of Hearts", "resources/images/7_of_hearts.png", 7)
    H8 = ("8 of Hearts", "resources/images/8_of_hearts.png", 8)
    H9 = ("9 of Hearts", "resources/images/9_of_hearts.png", 9)
    H10 = ("10 of Hearts", "resources/images/10_of_hearts.png", 10)
    H11 = ("Jack of Hearts", "resources/images/11_of_hearts.png", 11)
    H12 = ("Queen of Hearts", "resources/images/12_of_hearts.png", 12)
    H13 = ("King of Hearts", "resources/images/13_of_hearts.png", 13)

    # Diamonds - Karo
    D1 = ("Ace of Diamonds", "resources/images/1_of_diamonds.png", 1)
    D2 = ("2 of Diamonds", "resources/images/2_of_diamonds.png", 2)
    D3 = ("3 of Diamonds", "resources/images/3_of_diamonds.png", 3)
    D4 = ("4 of Diamonds", "resources/images/4_of_diamonds.png", 4)
    D5 = ("5 of Diamonds", "resources/images/5_of_diamonds.png", 5)
    D6 = ("6 of Diamonds", "resources/images/6_of_diamonds.png", 6)
    D7 = ("7 of Diamonds", "resources/images/7_of_diamonds.png", 7)
    D8 = ("8 of Diamonds", "resources/images/8_of_diamonds.png", 8)
    D9 = ("9 of Diamonds", "resources/images/9_of_diamonds.png", 9)
    D10 = ("10 of Diamonds", "resources/images/10_of_diamonds.png", 10)
    D11 = ("Jack of Diamonds", "resources/images/11_of_diamonds.png", 11)
    D12 = ("Queen of Diamonds", "resources/images/12_of_diamonds.png", 12)
    D13 = ("King of Diamonds", "resources/images/13_of_diamonds.png", 13)

    # Clubs - Trefl
    C1 = ("Ace of Clubs", "resources/images/1_of_clubs.png", 1)
    C2 = ("2 of Clubs", "resources/images/2_of_clubs.png", 2)
    C3 = ("3 of Clubs", "resources/images/3_of_clubs.png", 3)
    C4 = ("4 of Clubs", "resources/images/4_of_clubs.png", 4)
    C5 = ("5 of Clubs", "resources/images/5_of_clubs.png", 5)
    C6 = ("6 of Clubs", "resources/images/6_of_clubs.png", 6)
    C7 = ("7 of Clubs", "resources/images/7_of_clubs.png", 7)
    C8 = ("8 of Clubs", "resources/images/8_of_clubs.png", 8)
    C9 = ("9 of Clubs", "resources/images/9_of_clubs.png", 9)
    C10 = ("10 of Clubs", "resources/images/10_of_clubs.png", 10)
    C11 = ("Jack of Clubs", "resources/images/11_of_clubs.png", 11)
    C12 = ("Queen of Clubs", "resources/images/12_of_clubs.png", 12)
    C13 = ("King of Clubs", "resources/images/13_of_clubs.png", 13)

    # Spades - Pik
    S1 = ("Ace of Spades", "resources/images/1_of_spades.png", 1)
    S2 = ("2 of Spades", "resources/images/2_of_spades.png", 2)
    S3 = ("3 of Spades", "resources/images/3_of_spades.png", 3)
    S4 = ("4 of Spades", "resources/images/4_of_spades.png", 4)
    S5 = ("5 of Spades", "resources/images/5_of_spades.png", 5)
    S6 = ("6 of Spades", "resources/images/6_of_spades.png", 6)
    S7 = ("7 of Spades", "resources/images/7_of_spades.png", 7)
    S8 = ("8 of Spades", "resources/images/8_of_spades.png", 8)
    S9 = ("9 of Spades", "resources/images/9_of_spades.png", 9)
    S10 = ("10 of Spades", "resources/images/10_of_spades.png", 10)
    S11 = ("Jack of Spades", "resources/images/11_of_spades.png", 11)
    S12 = ("Queen of Spades", "resources/images/12_of_spades.png", 12)
    S13 = ("King of Spades", "resources/images/13_of_spades.png", 13)
