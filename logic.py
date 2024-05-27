# logic.py
from threading import Thread

from cards_data import CardsEnum
from card import Card
import time
import random

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
    gui_update_listener = None

    def __init__(self):
        self.gui = None

    # ===================== End of constructor =====================

    def set_gui(self, gui):
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

    def player_play(self, card_hand_index, update_callback):
        # check what cards are on top of gamestacks
        gm1_top_card = gamestack1[len(gamestack1) - 1]
        gm2_top_card = gamestack2[len(gamestack2) - 1]

        gm1_top_card_power = gm1_top_card.get_power()
        gm2_top_card_power = gm2_top_card.get_power()

        chosen_card = p1_hand[card_hand_index]
        player_card_power = chosen_card.get_power()
        can_play = False
        chosen_gamestack = -1

        # check if a play is possible with the chosen card
        if player_card_power + 1 == gm1_top_card_power or player_card_power - 1 == gm1_top_card_power:
            can_play = True
            chosen_gamestack = 1
        elif player_card_power + 1 == gm2_top_card_power or player_card_power - 1 == gm2_top_card_power:
            can_play = True
            chosen_gamestack = 2
        # ace card special case
        elif player_card_power == 1 and gm1_top_card_power == 13:
            can_play = True
            chosen_gamestack = 1
        elif player_card_power == 1 and gm2_top_card_power == 13:
            can_play = True
            chosen_gamestack = 2
        # king card special case
        elif player_card_power == 13 and gm1_top_card_power == 1:
            can_play = True
            chosen_gamestack = 1
        elif player_card_power == 13 and gm2_top_card_power == 1:
            can_play = True
            chosen_gamestack = 2

        if can_play:
            # remove the chosen card from the hand (play the card)
            p1_hand.pop(card_hand_index)
            # put the chosen card on the right gamestack
            if chosen_gamestack == 1:
                gamestack1.append(chosen_card)
            elif chosen_gamestack == 2:
                gamestack2.append(chosen_card)
            update_callback("player played a card")
        else:
            update_callback("player can't play this card")

    def player_draw(self, update_callback):
        if len(p1_supply) > 0:
            if len(p1_hand) < 5:
                p1_hand.append(p1_supply.pop())
                update_callback("player drew a card")
            else:
                print("You can't draw a card! Your hand is full!")

    # returns True if the computer played something, False if not
    def computer_play(self, player_hand, player_supply):
        can_play = False

        # check what cards are on top of gamestacks
        gm1_top_card = gamestack1[len(gamestack1) - 1]
        gm2_top_card = gamestack2[len(gamestack2) - 1]
        gm1_top_card_power = gm1_top_card.get_power()
        gm2_top_card_power = gm2_top_card.get_power()

        chosen_gamestack = -1
        # check if a play is possible
        for card in player_hand:
            player_card_power = card.get_power()
            if player_card_power + 1 == gm1_top_card_power or player_card_power - 1 == gm1_top_card_power:
                can_play = True
                chosen_gamestack = 1
                break
            elif player_card_power + 1 == gm2_top_card_power or player_card_power - 1 == gm2_top_card_power:
                can_play = True
                chosen_gamestack = 2
                break
            # ace card special case
            elif player_card_power == 1 and gm1_top_card_power == 13:
                can_play = True
                chosen_gamestack = 1
                break
            elif player_card_power == 1 and gm2_top_card_power == 13:
                can_play = True
                chosen_gamestack = 2
                break
            # king card special case
            elif player_card_power == 13 and gm1_top_card_power == 1:
                can_play = True
                chosen_gamestack = 1
                break
            elif player_card_power == 13 and gm2_top_card_power == 1:
                can_play = True
                chosen_gamestack = 2
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
            elif chosen_gamestack == 2:
                gamestack2.append(chosen_card)

            # draw a card from the supply to the hand
            if len(player_supply) > 0:
                player_hand.append(player_supply.pop())

            return True

        # if the computer can't play a card
        else:
            print("\nComputer can't play ANY card!")
            return False

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

    def computer_player(self):
        while self.game_running:
            self.computer_play(p2_hand, p2_supply)
            self.gui_update_listener("player 2 turn")
            time.sleep(self.computer_latency)

    def start_game(self, update_callback, computer_latency):
        self.init_new_game()
        update_callback("game started")

        # set the gui listener and latency for computer
        self.gui_update_listener = update_callback
        self.computer_latency = computer_latency

        # start the computer player thread
        computer_player_thread = Thread(target=self.computer_player)
        computer_player_thread.start()

        while self.game_running:

            # check if any player won the game (no cards in hand and supply)
            if len(p1_hand) == 0 and len(p1_supply) == 0:
                print("Player 1 won the game!")
                game_running = False
                break

            if len(p2_hand) == 0 and len(p2_supply) == 0:
                print("Player 2 won the game!")
                game_running = False
                break

            # computer action - separate thread TODO
            # self.computer_play(p2_hand, p2_supply)
            # update_callback("player 2 turn")
            # time.sleep(computer_latency)

            # can players play a card
            p1_state = self.can_player_play(p1_hand, p1_supply)
            p2_state = self.can_player_play(p1_hand, p1_supply)

            # check if both players cannot play a card
            if not p1_state and not p2_state:
                # if reshuffle stacks are empty, and no one can play a card, game is won by the player with the least cards in hand and supply
                if len(p1_reshuffle) == 0 and len(p2_reshuffle) == 0:
                    if len(p1_hand) + len(p1_supply) < len(p2_hand) + len(p2_supply):
                        print("Player 1 won the game!")
                        break
                    elif len(p1_hand) + len(p1_supply) > len(p2_hand) + len(p2_supply):
                        print("Player 2 won the game!")
                        break
                    else:
                        print("Game draw!")
                        break
                    # update_callback("game finished")
                    # game_running = False

                # reshuffle when no one can play a card
                print("No one can play a card! RESHUFFLE THE STACKS!")
                gamestack1.append(p1_reshuffle.pop())
                gamestack2.append(p2_reshuffle.pop())
                update_callback("reshuffle stacks")
                time.sleep(1)
