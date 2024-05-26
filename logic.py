# logic.py
from cards_data import CardsEnum
from card import Card
import time
import random

# player stacks
p1_hand = []  # 5 cards
p1_supply = []  # 13 cards at the start
p1_reshuffle = []  # 7 cards at the start

p2_hand = []  # 5 cards
p2_supply = []  # 13 cards at the start
p2_reshuffle = []  # 7 cards at the start

gamestack1 = []  # 1 card at the start
gamestack2 = []  # 1 card at the start

class GameLogic:
    def __init__(self):
        self.gui = None



        # Trigger GUI update (draw)
        # self.gui.update()

        # self.init_new_game()
        # self.gui.update()

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


    def player_play_test(self, card_hand_index, update_callback):
        chosen_card = p1_hand.pop(card_hand_index)
        gamestack1.append(chosen_card)
        update_callback("player played a card")

    def player_draw_test(self, update_callback):
        if len(p1_supply) > 0:
            p1_hand.append(p1_supply.pop())
            update_callback("player drew a card")

    # returns True if the player played something, False if not
    def player_turn(self, player_hand, player_supply):
        can_play = False

        # check what cards are on top of gamestacks
        gm1_top_card = gamestack1[len(gamestack1)-1]
        gm2_top_card = gamestack2[len(gamestack2)-1]

        gm1_top_card_power = gm1_top_card.get_power()
        gm2_top_card_power = gm2_top_card.get_power()

        # TODO Special checking for the ace card

        # check if a play is possible
        chosen_gamestack = -1
        for card in player_hand:
            player_card_power = card.get_power()
            if player_card_power + 1 == gm1_top_card_power or player_card_power - 1 == gm1_top_card_power:
                can_play = True
                chosen_gamestack = 1
                break
            if player_card_power + 1 == gm2_top_card_power or player_card_power - 1 == gm2_top_card_power:
                can_play = True
                chosen_gamestack = 2
                break

        if can_play:
            # let the player choose a card to play
            print("Player choses a card to play:")
            chosen_card_index = 1


            # check if the chosen card can be put on any of the gamestacks
            chosen_card_power = player_hand[chosen_card_index].get_power()
            if (chosen_card_power + 1 != gm1_top_card_power and chosen_card_power - 1 != gm1_top_card_power) \
                    and (chosen_card_power + 1 != gm2_top_card_power and chosen_card_power - 1 != gm2_top_card_power):
                print("You can't play THIS card!")
                # input("Press Enter to continue...")
                return False

            # remove the chosen card from the hand (play the card)
            chosen_card = player_hand.pop(chosen_card_index)

            # put the chosen card on the right gamestack
            if chosen_gamestack == 1:
                # gamestack1.clear()
                gamestack1.append(chosen_card)
            else:
                # gamestack2.clear()
                gamestack2.append(chosen_card)

# automatic card draw - to be scrapped and replaced with a function called by player click
            if len(player_supply) > 0:
                player_hand.append(player_supply.pop())

            return True

        # if the player can't play a card
        else:
            for i, card in enumerate(player_hand):
                print(f"{i + 1}) {card.name}")
            print("\nYou can't play ANY card!")
            input("Press Enter to continue...")
            return False


    # returns True if the computer played something, False if not
    def computer_turn(self, player_hand, player_supply):
        can_play = False

        # check what cards are on top of gamestacks
        gm1_top_card = gamestack1[len(gamestack1)-1]
        gm2_top_card = gamestack2[len(gamestack2)-1]

        gm1_top_card_power = gm1_top_card.get_power()
        gm2_top_card_power = gm2_top_card.get_power()

        # TODO Special checking for the ace card

        # check if a play is possible
        for card in player_hand:
            player_card_power = card.get_power()
            if player_card_power + 1 == gm1_top_card_power or player_card_power - 1 == gm1_top_card_power:
                can_play = True
                break
            if player_card_power + 1 == gm2_top_card_power or player_card_power - 1 == gm2_top_card_power:
                can_play = True
                break

        if can_play:
            # computer chooses a card to play
            chosen_card_index = -1
            chosen_gamestack = -1
            for i, card in enumerate(player_hand):
                if card.get_power() + 1 == gm1_top_card_power or card.get_power() - 1 == gm1_top_card_power:
                    chosen_card_index = i
                    chosen_gamestack = 1
                    break
                if card.get_power() + 1 == gm2_top_card_power or card.get_power() - 1 == gm2_top_card_power:
                    chosen_card_index = i
                    chosen_gamestack = 2
                    break

            # remove the chosen card from the hand (play the card)
            chosen_card = player_hand.pop(chosen_card_index)

            # put the chosen card on the right gamestack
            if chosen_gamestack == 1:
                gamestack1.clear()
                gamestack1.append(chosen_card)
            else:
                gamestack2.clear()
                gamestack2.append(chosen_card)

            # draw a card from the supply to the hand
            if len(player_supply) > 0:
                player_hand.append(player_supply.pop())

            return True

        # if the computer can't play a card
        else:
            print("\nComputer can't play ANY card!")
            input("Press Enter to continue...")
            return False


# ===================== Command line methods =====================

    def cls(self):
        print("\n" * 20)

    def print_game_table(self):
        print("PLAYER 2 🟥                 ", end="")
        print("🎁" + str(len(p2_supply)), end="")
        print("     ✋" + str(len(p2_hand)))
        print()
        print("                 " + str(len(p2_reshuffle)) + "🔃     " + str(gamestack1[0]) + " | " + str(
            gamestack2[0]) + "     🔃" + str(len(p1_reshuffle)))
        print()
        print("PLAYER 1 🟩                 ", end="")
        print("✋" + str(len(p1_hand)), end="")
        print("     🎁" + str(len(p1_supply)))

# ===================== Main game loop =====================

    def start_game(self, update_callback):
        self.init_new_game()

        game_running = True

        while game_running:
            update_callback("game started")

            # self.print_game_table()

            # check if any player won the game (no cards in hand and supply)
            if len(p1_hand) == 0 and len(p1_supply) == 0:
                print("Player 1 won the game!")
                game_running = False

            if len(p2_hand) == 0 and len(p2_supply) == 0:
                print("Player 2 won the game!")
                game_running = False

            print("\n============================ Player 1 turn ============================")
            p1_state = self.player_turn(p1_hand, p1_supply)
            # print(p1_hand)
            # self.cls()
            update_callback("player 1 turn")

            # player 2 turn (computer)
            print("============================ Computer turn ============================")
            p2_state = self.computer_turn(p2_hand, p2_supply)
            time.sleep(1)

            # self.cls()
            update_callback("player 2 turn")

            # check if both players didn't play a card
            if not p1_state and not p2_state:
                # self.cls()
                print("No one can play a card! RESHUFFLE THE STACKS!")
                update_callback("reshuffle stacks")
                time.sleep(1)


                # check if there are cards to reshuffle
                if len(p1_reshuffle) == 0 and len(p2_reshuffle) == 0:
                    print("No more cards to reshuffle! Game draw!")
                    update_callback("game finished")
                    game_running = False

                gamestack1.append(p1_reshuffle.pop())
                gamestack2.append(p2_reshuffle.pop())

                # if reshuffle stacks are empty, and no one can play a card, game is won by the player with the least cards in hand and supply
                if len(p1_reshuffle) == 0 and len(p2_reshuffle) == 0:
                    if len(p1_hand) + len(p1_supply) < len(p2_hand) + len(p2_supply):
                        print("Player 1 won the game!")
                    elif len(p1_hand) + len(p1_supply) > len(p2_hand) + len(p2_supply):
                        print("Player 2 won the game!")
                    else:
                        print("Game draw!")
                    update_callback("game finished")
                    game_running = False
