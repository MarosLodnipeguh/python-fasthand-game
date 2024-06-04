from threading import Thread
import time
import random

from models.cards_data import CardsEnum
from models.card import Card
from events_and_listeners.event_listener import EventListener

# Initialize player's hand, supply, reshuffle stack and game stacks
p1_hand = [Card]  # 5 cards
p1_supply = [Card]  # 13 cards at the start
p1_reshuffle = [Card]  # 7 cards at the start
p2_hand = [Card]  # 5 cards
p2_supply = [Card]  # 13 cards at the start
p2_reshuffle = [Card]  # 7 cards at the start
gamestack1 = [Card]  # 1 card at the start
gamestack2 = [Card]  # 1 card at the start


class GameLogic:
    """
    The GameLogic class handles the logic of the card game.
    It manages the game state, player actions, and computer player logic.
    """
    game_running: bool = False
    computer_latency: float = -1

    # ==================== Constructor ====================
    def __init__(self, gui: EventListener = None):
        """
        Initialize the GameLogic class.
        :param gui: The GUI object that will be used to interact with the game, initially None.
        """
        self.gui = gui

    def set_gui(self, gui: EventListener):
        """
        Set the GUI object and share the game state lists with it.
        :param gui: The GameGUI object that will be used to interact with the game.
        """
        self.gui = gui
        gui.set_shared_lists(p1_hand, p1_supply, p1_reshuffle,
                             p2_hand, p2_supply, p2_reshuffle,
                             gamestack1, gamestack2)

    # ==================== Game Initialization ====================
    def init_new_game(self):
        """
        Initialize a new game by creating a deck of cards, shuffling it, and distributing the cards to the players lists.
        """
        # fill the deck with all the cards
        deck = []
        for entry in CardsEnum:
            new_card = Card(entry.name, entry.full_name, entry.image_path, entry.power)
            deck.append(new_card)

        # shuffle the deck
        random.shuffle(deck)

        # clear player stacks
        p1_hand.clear()
        p1_supply.clear()
        gamestack1.clear()
        p1_reshuffle.clear()
        p2_hand.clear()
        p2_supply.clear()
        gamestack2.clear()
        p2_reshuffle.clear()

        # init player stacks
        for i in range(5):
            p1_hand.append(deck.pop())
            p2_hand.append(deck.pop())

        for i in range(13):
            p1_supply.append(deck.pop())
            p2_supply.append(deck.pop())

        gamestack1.append(deck.pop())
        gamestack2.append(deck.pop())

        for i in range(7):
            p1_reshuffle.append(deck.pop())
            p2_reshuffle.append(deck.pop())

    # ==================== Player Actions ====================
    def player_put(self, chosen_card_index: int, chosen_gamestack_index: int):
        """
        Handle the player's action to play a card.
        :param chosen_card_index: The index of the card that the player chose to play.
        :param chosen_gamestack_index: The index of the game stack that the player chose to play the card on.
        """
        # get the chosen gamestack
        chosen_gamestack = None
        if chosen_gamestack_index == 1:
            chosen_gamestack = gamestack1
        elif chosen_gamestack_index == 2:
            chosen_gamestack = gamestack2

        # check the power of the top card of the chosen gamestack
        gamestack_top_card = chosen_gamestack[len(chosen_gamestack) - 1]
        gamestack_top_card_power = gamestack_top_card.get_power()

        # get the power of player's chosen card
        chosen_card = p1_hand[chosen_card_index]
        player_card_power = chosen_card.get_power()

        # check if a play is possible with the chosen card
        if player_card_power + 1 == gamestack_top_card_power or player_card_power - 1 == gamestack_top_card_power:
            p1_hand.pop(chosen_card_index)
            chosen_gamestack.append(chosen_card)
            self.gui.repaint()
        # ace card special case
        elif player_card_power == 1 and gamestack_top_card_power == 13:
            p1_hand.pop(chosen_card_index)
            chosen_gamestack.append(chosen_card)
            self.gui.repaint()
        # king card special case
        elif player_card_power == 13 and gamestack_top_card_power == 1:
            p1_hand.pop(chosen_card_index)
            chosen_gamestack.append(chosen_card)
            self.gui.repaint()
        else:
            print("You can't play this card!")

    def player_draw(self):
        """
        Handle the player's action to draw a card.
        """
        if len(p1_supply) > 0:
            if len(p1_hand) < 5:
                p1_hand.append(p1_supply.pop())
                self.gui.repaint()
            else:
                print("You can't draw! Your hand is full!")

    # ==================== Computer Player Thread ====================
    def computer_play(self, player_hand: [Card], player_supply: [Card]):
        """
        Handle the computer's action to play a card.
        :param player_hand: The hand of the computer player.
        :param player_supply: The supply of the computer player.
        :return: True if the computer put or draw a card (for gui repainting), False if not.
        """

        # check what cards are on top of gamestacks
        gm1_top_card = gamestack1[len(gamestack1) - 1]
        gm2_top_card = gamestack2[len(gamestack2) - 1]
        gm1_top_card_power = gm1_top_card.get_power()
        gm2_top_card_power = gm2_top_card.get_power()

        for i, card in enumerate(player_hand):
            player_card_power = card.get_power()
            if player_card_power + 1 == gm1_top_card_power or player_card_power - 1 == gm1_top_card_power:
                self.computer_put(i, 1)
                return True
            elif player_card_power + 1 == gm2_top_card_power or player_card_power - 1 == gm2_top_card_power:
                self.computer_put(i, 2)
                return True
            # ace card special case
            elif player_card_power == 1 and gm1_top_card_power == 13:
                self.computer_put(i, 1)
                return True
            elif player_card_power == 1 and gm2_top_card_power == 13:
                self.computer_put(i, 2)
                return True
            # king card special case
            elif player_card_power == 13 and gm1_top_card_power == 1:
                self.computer_put(i, 1)
                return True
            elif player_card_power == 13 and gm2_top_card_power == 1:
                self.computer_put(i, 2)
                return True
            # if the computer can't play a card, draw a card
            elif len(player_hand) < 5 and len(player_supply) > 0:
                p2_hand.append(p2_supply.pop())
                return True
            # else:
                # print("Computer can't play a card!")
        # after checking all cards in loop
        return False

    def computer_put(self, chosen_card_index: int, chosen_gamestack: int):
        """
        Handle the computer's action to put a card on a gamestack.
        :param chosen_gamestack: The index of the game stack that the computer chose to play the card on.
        :param chosen_card_index: The index of the card that the computer chose to play.
        """
        if chosen_gamestack == 1:
            gamestack1.append(p2_hand.pop(chosen_card_index))
        elif chosen_gamestack == 2:
            gamestack2.append(p2_hand.pop(chosen_card_index))
        else:
            print("Invalid gamestack index!")

    def computer_player(self):
        """
        The main loop for the computer player thread.
        It waits for a certain latency, then tries to play a card.
        If the computer played a card, the GUI update is called.
        """

        # wait before the computer starts playing
        time.sleep(2)

        while self.game_running:
            # try to play a card
            played = self.computer_play(p2_hand, p2_supply)
            if played:
                self.gui.repaint()

            time.sleep(self.computer_latency)

    # ==================== Main Game loop ====================
    def can_player_act(self, player_hand: [Card], player_suuply: [Card]):
        """
        Check if the player can play or draw a card.
        :param player_hand: The hand of the player.
        :param player_suuply: The supply of the player.
        :return: True if the player can play or draw a card, False if not.
        """

        # check if the player can draw a card
        if len(player_hand) < 5 and len(player_suuply) > 0:
            return True
        else:
            # check what cards are on top of gamestacks
            gm1_top_card = gamestack1[len(gamestack1) - 1]
            gm2_top_card = gamestack2[len(gamestack2) - 1]
            gm1_top_card_power = gm1_top_card.get_power()
            gm2_top_card_power = gm2_top_card.get_power()

            # check if a play is possible
            for card in player_hand:
                player_card_power = card.get_power()
                if player_card_power + 1 == gm1_top_card_power or player_card_power - 1 == gm1_top_card_power:
                    return True
                elif player_card_power + 1 == gm2_top_card_power or player_card_power - 1 == gm2_top_card_power:
                    return True
                # ace card special case
                elif player_card_power == 1 and gm1_top_card_power == 13:
                    return True
                elif player_card_power == 1 and gm2_top_card_power == 13:
                    return True
                # king card special case
                elif player_card_power == 13 and gm1_top_card_power == 1:
                    return True
                elif player_card_power == 13 and gm2_top_card_power == 1:
                    return True
            # if the player can't play a card
            return False

    def start_game(self, computer_latency: float):
        """
        Start the main game loop.
        It checks if players can play a card and if any player won the game.
        :param computer_latency: The latency of the computer player.
        """
        self.init_new_game()
        self.gui.repaint()

        # set game variables
        self.game_running = True
        self.computer_latency = computer_latency

        # start the computer player thread
        computer_player_thread = Thread(target=self.computer_player)
        computer_player_thread.start()

        # loop checking the game state
        while self.game_running:
            time.sleep(1)

            # check if any player won the game (no cards in hand and supply)
            if len(p1_hand) == 0 and len(p1_supply) == 0:
                print("Player 1 won the game!")
                self.game_running = False
                self.gui.player_1_wins()
                break

            if len(p2_hand) == 0 and len(p2_supply) == 0:
                print("Player 2 won the game!")
                self.game_running = False
                self.gui.player_2_wins()
                break

            # can players play a card
            can_p1_act = self.can_player_act(p1_hand, p1_supply)
            can_p2_act = self.can_player_act(p2_hand, p2_supply)

            # check if both players cannot play a card
            if not can_p1_act and not can_p2_act:
                # end the game and check who won if reshuffle stacks are empty and no one can play a card
                if len(p1_reshuffle) == 0 and len(p2_reshuffle) == 0:
                    if len(p1_hand) + len(p1_supply) < len(p2_hand) + len(p2_supply):
                        print("Player 1 won the game!")
                        self.game_running = False
                        self.gui.player_1_wins()
                        break
                    elif len(p1_hand) + len(p1_supply) > len(p2_hand) + len(p2_supply):
                        print("Player 2 won the game!")
                        self.game_running = False
                        self.gui.player_2_wins()
                        break
                    else:
                        print("Game draw!")
                        self.game_running = False
                        self.gui.game_draw()
                        break
                else:
                    # reshuffle the stacks
                    self.call_reshuffle()

    def call_reshuffle(self):
        """
        Call the GUI for reshuffling the game stacks and wait for response from player, only after that continue the game
        """
        print("No one can play a card! Reshuffle the game stacks!")
        self.gui.reshuffle_call()

    def accept_reshuffle(self):
        """
        Accept the reshuffling of the game stacks. Called by the GUI.
        """
        gamestack1.append(p1_reshuffle.pop())
        gamestack2.append(p2_reshuffle.pop())
        self.gui.reshuffle_done()

    def close_game(self):
        """
        Close the game and exit the program.
        """
        self.game_running = False
        exit(0)
