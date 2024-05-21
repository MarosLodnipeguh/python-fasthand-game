from cards import Card
import time
import random


def cls():
    print("\n" * 20)


# player stacks
p1_hand = []  # 5 cards
p1_supply = []  # 13 cards at the start
p1_reshuffle = []  # 7 cards at the start

p2_hand = []  # 5 cards
p2_supply = []  # 13 cards at the start
p2_reshuffle = []  # 7 cards at the start

gamestack1 = []  # 1 card at the start
gamestack2 = []  # 1 card at the start


def init_new_game():
    # fill the deck with all the cards
    deck = []
    for card in Card:
        deck.append(card)

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


def get_card_number(card):
    return int(''.join(filter(str.isdigit, str(card))))


# returns True if the player played something, False if not
def player_turn(player_hand, player_supply):
    can_play = False

    # check what numbers the player has
    player_hand_numbers = []
    for card in player_hand:
        number_part = get_card_number(card)
        player_hand_numbers.append(number_part)

    # check what number of cards are on the gamestacks
    gamestack1_number = get_card_number(gamestack1[0])
    gamestack2_number = get_card_number(gamestack2[0])

    # check if a play is possible
    chosen_gamestack = -1
    for number in player_hand_numbers:
        if number + 1 == gamestack1_number or number - 1 == gamestack1_number:
            can_play = True
            chosen_gamestack = 1
            break
        if number + 1 == gamestack2_number or number - 1 == gamestack2_number:
            can_play = True
            chosen_gamestack = 2
            break

    if can_play:
        # let the player choose a card to play
        print("Choose a card to play:")
        for i, card in enumerate(player_hand):
            print(f"{i + 1}) {card.value}" + f" ({get_card_number(card)})")

        chosen_card_index = int(input("type: ")) - 1

        # check if the chosen card can be put on any of the gamestacks
        chosen_card_number = player_hand_numbers[chosen_card_index]
        if (chosen_card_number + 1 != gamestack1_number and chosen_card_number - 1 != gamestack1_number) \
                and (chosen_card_number + 1 != gamestack2_number and chosen_card_number - 1 != gamestack2_number):
            print("You can't play THIS card!")
            input("Press Enter to continue...")
            return False

        # remove the chosen card from the hand (play the card)
        chosen_card = player_hand.pop(chosen_card_index)

        # put the chosen card on the right gamestack
        if chosen_gamestack == 1:
            gamestack1.clear()
            gamestack1.append(chosen_card)
        else:
            gamestack2.clear()
            gamestack2.append(chosen_card)

        if len(player_supply) > 0:
            player_hand.append(player_supply.pop())

        return True

    # if the player can't play a card
    else:
        for i, card in enumerate(player_hand):
            print(f"{i + 1}) {card.value}" + f" ({get_card_number(card)})")
        print("\nYou can't play ANY card!")
        input("Press Enter to continue...")
        return False


# returns True if the computer played something, False if not
def computer_turn(player_hand, player_supply):
    can_play = False

    # check what numbers the player has
    player_hand_numbers = []
    for card in player_hand:
        number_part = get_card_number(card)
        player_hand_numbers.append(number_part)

    # check what number of cards are on the gamestacks
    gamestack1_number = get_card_number(gamestack1[0])
    gamestack2_number = get_card_number(gamestack2[0])

    # check if a play is possible
    for number in player_hand_numbers:
        if number + 1 == gamestack1_number or number - 1 == gamestack1_number:
            can_play = True
        if number + 1 == gamestack2_number or number - 1 == gamestack2_number:
            can_play = True

    if can_play:
        # computer chooses a card to play
        chosen_card_index = -1
        chosen_gamestack = -1
        for i, card in enumerate(player_hand):
            if get_card_number(card) + 1 == gamestack1_number or get_card_number(card) - 1 == gamestack1_number:
                chosen_card_index = i
                chosen_gamestack = 1
                break
            if get_card_number(card) + 1 == gamestack2_number or get_card_number(card) - 1 == gamestack2_number:
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


def print_game_table():
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


def main():
    init_new_game()

    game_running = True

    while game_running:
        print_game_table()

        # check if any player won the game (no cards in hand and supply)
        if len(p1_hand) == 0 and len(p1_supply) == 0:
            print("Player 1 won the game!")
            game_running = False

        if len(p2_hand) == 0 and len(p2_supply) == 0:
            print("Player 2 won the game!")
            game_running = False

        print("\n============================ Player 1 turn ============================")
        p1_state = player_turn(p1_hand, p1_supply)
        # print(p1_hand)
        cls()

        # player 2 turn (computer)
        print("============================ Computer turn ============================")
        p2_state = computer_turn(p2_hand, p2_supply)
        time.sleep(1)

        cls()

        # check if both players didn't play a card
        if not p1_state and not p2_state:
            cls()
            print("No one can play a card! RESHUFFLE THE STACKS!")
            time.sleep(1)

            # check if there are cards to reshuffle
            if len(p1_reshuffle) == 0 and len(p2_reshuffle) == 0:
                print("No more cards to reshuffle! Game draw!")
                game_running = False

            gamestack1[0] = p1_reshuffle.pop()
            gamestack2[0] = p2_reshuffle.pop()

            # if reshuffle stacks are empty, and no one can play a card, game is won by the player with the least cards in hand and supply
            if len(p1_reshuffle) == 0 and len(p2_reshuffle) == 0:
                if len(p1_hand) + len(p1_supply) < len(p2_hand) + len(p2_supply):
                    print("Player 1 won the game!")
                elif len(p1_hand) + len(p1_supply) > len(p2_hand) + len(p2_supply):
                    print("Player 2 won the game!")
                else:
                    print("Game draw!")
                game_running = False


if __name__ == '__main__':
    main()
