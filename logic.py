from threading import Thread
import time
import random

from models.cards_data import CardsEnum
from models.card import Card
from events_and_listeners.event_listener import EventListener

p1_hand = []  # 5 cards
p1_supply = []  # 13 cards at the start
p1_reshuffle = []  # 7 cards at the start
p2_hand = []  # 5 cards
p2_supply = []  # 13 cards at the start
p2_reshuffle = []  # 7 cards at the start
gamestack1 = []  # 1 card at the start
gamestack2 = []  # 1 card at the start


class GameLogic:
    game_running = True
    computer_latency = -1

    def __init__(self, gui: EventListener = None):
        self.gui = gui

        # self.p1 = Player()
        # self.p2 = Player()
        #
        # self.gm1 = GameStack()
        # self.gm2 = GameStack()

    # ===================== End of constructor =====================

    def set_gui(self, gui: EventListener):
        self.gui = gui
        # Share these lists with the GUI
        gui.set_shared_lists(p1_hand, p1_supply, p1_reshuffle,
                             p2_hand, p2_supply, p2_reshuffle,
                             gamestack1, gamestack2)

    def init_new_game(self):
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

    # ===================== Player actions =====================
    def player_play(self, chosen_card_index, chosen_gamestack_index):
        # if chosen_gamestack_index is None:
        #     update_callback("player didn't choose a gamestack")
        #     return

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
        if len(p1_supply) > 0:
            if len(p1_hand) < 5:
                p1_hand.append(p1_supply.pop())
                self.gui.repaint()
            else:
                print("You can't draw! Your hand is full!")

    # ===================== Computer player logic =====================

    # returns True if the computer played something, False if not
    def computer_play(self, player_hand, player_supply):
        can_play = False

        # check what cards are on top of gamestacks
        gm1_top_card = gamestack1[len(gamestack1) - 1]
        gm2_top_card = gamestack2[len(gamestack2) - 1]
        gm1_top_card_power = gm1_top_card.get_power()
        gm2_top_card_power = gm2_top_card.get_power()

        # check if a play is possible
        for card in player_hand:
            player_card_power = card.get_power()
            if player_card_power + 1 == gm1_top_card_power or player_card_power - 1 == gm1_top_card_power:
                can_play = True
                break
            elif player_card_power + 1 == gm2_top_card_power or player_card_power - 1 == gm2_top_card_power:
                can_play = True
                break
            # ace card special case
            elif player_card_power == 1 and gm1_top_card_power == 13:
                can_play = True
                break
            elif player_card_power == 1 and gm2_top_card_power == 13:
                can_play = True
                break
            # king card special case
            elif player_card_power == 13 and gm1_top_card_power == 1:
                can_play = True
                break
            elif player_card_power == 13 and gm2_top_card_power == 1:
                can_play = True
                break

        if can_play:
            # computer chooses a card to play
            chosen_card_index = -1
            chosen_gamestack = -1
            for i, card in enumerate(player_hand):
                player_card_power = card.get_power()
                if player_card_power + 1 == gm1_top_card_power or player_card_power - 1 == gm1_top_card_power:
                    chosen_card_index = i
                    chosen_gamestack = 1
                    break
                elif player_card_power + 1 == gm2_top_card_power or player_card_power - 1 == gm2_top_card_power:
                    chosen_card_index = i
                    chosen_gamestack = 2
                    break
                # ace card special case
                elif player_card_power == 1 and gm1_top_card_power == 13:
                    chosen_card_index = i
                    chosen_gamestack = 1
                    break
                elif player_card_power == 1 and gm2_top_card_power == 13:
                    chosen_card_index = i
                    chosen_gamestack = 2
                    break
                # king card special case
                elif player_card_power == 13 and gm1_top_card_power == 1:
                    chosen_card_index = i
                    chosen_gamestack = 1
                    break
                elif player_card_power == 13 and gm2_top_card_power == 1:
                    chosen_card_index = i
                    chosen_gamestack = 2
                    break

            # remove the chosen card from the hand (play the card)
            chosen_card = player_hand.pop(chosen_card_index)

            # put the chosen card on the right gamestack
            if chosen_gamestack == 1:
                gamestack1.append(chosen_card)
                self.gui.repaint()
            elif chosen_gamestack == 2:
                gamestack2.append(chosen_card)
                self.gui.repaint()

            # wait before drawing a card
            time.sleep(1)

            # draw a card from the supply to the hand
            if len(player_supply) > 0:
                player_hand.append(player_supply.pop())

            return True

        # if the computer can't play a card
        else:
            # print("\nComputer can't play ANY card!")
            return False

    def computer_player(self):
        # wait 3 seconds before the computer starts playing
        time.sleep(2)

        while self.game_running:
            time.sleep(self.computer_latency)

            play = self.computer_play(p2_hand, p2_supply)
            if play:
                self.gui.repaint()

    # ===================== Main game loop =====================

    def can_player_play(self, player_hand, player_suuply):
        # check what cards are on top of gamestacks
        gm1_top_card = gamestack1[len(gamestack1) - 1]
        gm2_top_card = gamestack2[len(gamestack2) - 1]
        gm1_top_card_power = gm1_top_card.get_power()
        gm2_top_card_power = gm2_top_card.get_power()

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
        return False

    def start_game(self, computer_latency):
        self.init_new_game()
        self.gui.repaint()

        # set latency for computer
        self.computer_latency = computer_latency

        # start the computer player thread
        computer_player_thread = Thread(target=self.computer_player)
        computer_player_thread.start()

        # loop checking if a player won the game or if the game is a draw
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
            p1_state = self.can_player_play(p1_hand, p1_supply)
            p2_state = self.can_player_play(p1_hand, p1_supply)

            # check if both players cannot play a card
            if not p1_state and not p2_state:

                # case when both players have full hands
                if len(p1_hand) == 5 and len(p2_hand) == 5:
                    self.call_reshuffle()

                # case when only one player has empty supply but both players cant play a card
                if len(p1_supply) == 0 and len(p2_supply) > 0:
                    self.call_reshuffle()
                elif len(p1_supply) > 0 and len(p2_supply) == 0:
                    self.call_reshuffle()

                # case when both players have empty supplies and cant play a card
                if len(p1_supply) == 0 and len(p2_supply) == 0:
                    self.call_reshuffle()

                # if reshuffle stacks are empty, and no one can play a card, game is won by the player with the least cards in hand and supply
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

    def call_reshuffle(self):
        print("No one can play a card! RESHUFFLE THE STACKS!")
        # send the event to the GUI and wait for response from player, only after that continue the game
        self.gui.reshuffle_call()

    def accept_reshuffle(self):
        gamestack1.append(p1_reshuffle.pop())
        gamestack2.append(p2_reshuffle.pop())
        self.gui.reshuffle_done()

    def close_game(self):
        self.game_running = False
        exit(0)
