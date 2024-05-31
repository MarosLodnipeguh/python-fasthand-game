import os
import tkinter as tk
from enum import Enum

from PIL import Image, ImageTk
from threading import Thread
from events_and_listeners.click_event import ClickEvent
from events_and_listeners.event_listener import EventListener


class GameState(Enum):
    READY = 1
    GAME_IN_PROGRESS = 2
    WAITING_FOR_RESHUFFLE = 3
    PLAYER_1_WINS = 4
    PLAYER_2_WINS = 5
    GAME_DRAW = 6


class EventName(Enum):
    CHOOSE_CARD = 1
    PUT_CARD = 2
    DRAW_CARD = 3
    RESHUFFLE = 4


class GameGUI(EventListener):
    # Constants for layout
    CARD_WIDTH = 120  # Adjust based on your card image dimensions
    CARD_HEIGHT = 180  # Adjust based on your card image dimensions
    SCREEN_WIDTH = 1125
    SCREEN_HEIGHT = 750

    # GUI components
    canvas = None
    card_images = {}  # key: image_path, value: photo
    clickable_items = {}  # key: card_image, value: click_event (type of action and card index in its list)
    clickable_highlight_rect = None

    # global chosen card to be remembered between gui updates
    chosen_card_index = None
    chosen_card = None  # card_image
    chosen_highlight_rect = None

    # variables passed to the logic
    computer_latency = 1
    game_state = GameState.READY

    # shared lists between GUI and logic
    p1_hand = []
    p1_supply = []
    p1_reshuffle = []
    p2_hand = []
    p2_supply = []
    p2_reshuffle = []
    gamestack1 = []
    gamestack2 = []

    # ===================== Constructor ====================
    def __init__(self, logic):
        self.logic = logic

        self.root = tk.Tk()
        self.root.title("Speed Card Game ♠ ♥ ♣ ♦")
        self.root.protocol("WM_DELETE_WINDOW", self.close_game)

        # UI components
        self.canvas = tk.Canvas(self.root, width=self.SCREEN_WIDTH, height=self.SCREEN_HEIGHT, bg='green')
        self.canvas.pack()

        # Welcome screen
        button = tk.Button(self.root, text="Start the game", command=self.start_game)
        self.canvas.create_window(600, 300, window=button)

        self.canvas.create_text(600, 365, text="Set the computer latency:", font=("Helvetica", 12, "bold"),
                                fill="white")

        slider = tk.Scale(self.root, from_=0.1, to=10, orient='horizontal', resolution=0.1,
                          command=self.set_computer_latency)
        self.canvas.create_window(600, 400, window=slider)

        # Load card images into memory
        self.load_card_images()

        # Create a highlight rectangles (initially hidden)
        self.create_clickable_highlight_rect()
        self.create_chosen_highlight_rect()

        # Bind mouse motion and click events
        self.canvas.bind('<Motion>', self.highlight_playable_cards)
        self.canvas.bind('<Button-1>', self.on_click)

    # ===================== GUI initialization functions ====================
    def set_shared_lists(self, p1_h, p1_s, p1_r, p2_h, p2_s, p2_r, g1, g2):
        self.p1_hand = p1_h
        self.p1_supply = p1_s
        self.p1_reshuffle = p1_r
        self.p2_hand = p2_h
        self.p2_supply = p2_s
        self.p2_reshuffle = p2_r
        self.gamestack1 = g1
        self.gamestack2 = g2

    def load_card_images(self):
        folder_path = 'resources/images'
        # List all files in the specified directory
        filenames = os.listdir(folder_path)
        # Filter out directories and include the full path for files
        file_list = [os.path.join(folder_path, f) for f in filenames if os.path.isfile(os.path.join(folder_path, f))]
        # scale the images to the same size
        for path in file_list:
            image = Image.open(path)
            image = image.resize((self.CARD_WIDTH, self.CARD_HEIGHT))  # Resize the image to 100x100 pixels
            photo = ImageTk.PhotoImage(image)
            path = path.replace("\\", "/")
            self.card_images[path] = photo

    def set_computer_latency(self, value):
        float_value = float(value)
        self.computer_latency = float_value

    def create_clickable_highlight_rect(self):
        self.clickable_highlight_rect = self.canvas.create_rectangle(0, 0, 0, 0, outline='yellow', width=3,
                                                                     state='hidden')

    def create_chosen_highlight_rect(self):
        self.chosen_highlight_rect = self.canvas.create_rectangle(0, 0, 0, 0, outline='orange', width=3, state='hidden')

    def run(self):
        self.root.mainloop()

    # ===================== Game loop functions ====================
    def start_game(self):
        self.game_state = GameState.GAME_IN_PROGRESS
        # Create and start the game loop thread
        game_thread = Thread(target=self.run_game)
        game_thread.start()
        self.repaint_canvas()

    def run_game(self):
        # Start the game loop passing the chosen computer latency to the logic
        self.logic.start_game(self.computer_latency)

    def close_game(self):
        self.root.destroy()
        self.logic.close_game()

    # ===================== GUI mouse hover and click functions ====================

    def bind_hover_events(self, card_id):
        self.canvas.tag_bind(card_id, "<Enter>", lambda event, cid=card_id: self.on_hover(cid))
        self.canvas.tag_bind(card_id, "<Leave>", lambda event, cid=card_id: self.on_leave(cid))

    def bind_click_events(self, card_id):
        self.canvas.tag_bind(card_id, "<Button-1>", lambda event, cid=card_id: self.on_click(cid))

    def on_hover(self, card_id):
        if card_id in self.clickable_items:
            self.canvas.itemconfig(card_id, outline="yellow")

    def on_leave(self, card_id):
        if card_id not in self.selected_cards:
            self.canvas.itemconfig(card_id, outline="")

    def on_click(self, card_id):
        if card_id in self.selected_cards:
            self.selected_cards.remove(card_id)
            self.canvas.itemconfig(card_id, outline="")
        else:
            self.selected_cards.add(card_id)
            self.canvas.itemconfig(card_id, outline="orange")



    # Function to handle card highlight on mouse move
    def highlight_playable_cards(self, event):
        canvas = self.canvas  # Alias for self.canvas
        highlight_rect = self.clickable_highlight_rect  # Alias for self.highlight_id

        for key in self.clickable_items:
            card_image = key
            # Check if mouse is inside the card's bounding box
            if canvas.bbox(card_image) and canvas.bbox(card_image)[0] <= event.x <= canvas.bbox(card_image)[2] and \
                    canvas.bbox(card_image)[1] <= event.y <= canvas.bbox(card_image)[3]:
                canvas.itemconfig(highlight_rect, state='normal')
                canvas.coords(highlight_rect, canvas.bbox(card_image))
                break
            else:
                canvas.itemconfig(highlight_rect, state='hidden')

    # TODO: on every gui update, the highlight rect vanishes
    def highlight_chosen_card(self, canvas, chosen_card_image):
        if chosen_card_image is not None:

            canvas.coords(self.chosen_highlight_rect, canvas.bbox(chosen_card_image))
            canvas.itemconfig(self.chosen_highlight_rect, state='normal')
            # highlight_rect = canvas.create_rectangle(0, 0, 0, 0, outline='orange', width=3, state='normal', tags='top')
            canvas.tag_raise(self.chosen_highlight_rect)

            # print("should highlight")
            canvas.create_rectangle(10, 10, 10, 10, outline='orange', width=3, state='normal')
            # canvas.create_text(90, 500, text="a card is chosen", font=("Helvetica", 12, "bold"), fill="white")
        # else:
        #     canvas.create_text(90, 500, text="not chosen", font=("Helvetica", 12, "bold"), fill="white")

    # Function to handle the click event (call the image_click_function when any of clickable items is clicked)
    def on_click(self, event):
        canvas = self.canvas  # Alias for self.canvas
        for key, value in self.clickable_items.items():  # key: card_image, value: click_event
            card_id = key
            bbox = canvas.bbox(card_id)
            if bbox and bbox[0] <= event.x <= bbox[2] and bbox[1] <= event.y <= bbox[3]:
                self.click_event_handler(key, value)
                break

    # Function called when a clickable item is clicked
    def click_event_handler(self, card_image, click_event):
        if click_event.get_name() == "CHOOSE CARD":
            self.chosen_card_index = click_event.get_index()
            self.chosen_card = card_image
            self.repaint_canvas()
            # self.highlight_chosen_card(self.canvas, self.chosen_card)

        elif click_event.get_name() == "PUT CARD":
            if self.chosen_card is None or self.chosen_card_index is None:
                print("Choose a card first!")
                return
            else:
                chosen_gamestack_index = click_event.get_index()
                self.logic.player_play(self.chosen_card_index, chosen_gamestack_index)
                # clear the chosen card after playing it
                self.chosen_card_index = None
                self.chosen_card = None

        elif click_event.get_name() == "DRAW CARD":
            self.logic.player_draw()

        elif click_event.get_name() == "RESHUFFLE":
            if self.game_state == GameState.WAITING_FOR_RESHUFFLE:
                self.logic.accept_reshuffle()
            else:
                print("You can't reshuffle now!")

    # ===================== GUI drawing functions ====================
    def draw_gameboard(self, canvas, card_images):

        blue_reverse_path = "resources/images/0_reverse_blue.png"
        red_reverse_path = "resources/images/0_reverse_red.png"

        # draw game state notification
        # if self.game_state == GameState.GAME_IN_PROGRESS:
        #     pass
        if self.game_state == GameState.WAITING_FOR_RESHUFFLE:
            self.canvas.create_text(90, 400, text="Waiting for reshuffle", font=("Helvetica", 12, "bold"), fill="white")
        elif self.game_state == GameState.PLAYER_1_WINS:
            self.canvas.create_text(90, 400, text="Player 1 wins!", font=("Helvetica", 12, "bold"), fill="white")
        elif self.game_state == GameState.PLAYER_2_WINS:
            self.canvas.create_text(90, 400, text="Player 2 wins!", font=("Helvetica", 12, "bold"), fill="white")
        elif self.game_state == GameState.GAME_DRAW:
            self.canvas.create_text(90, 400, text="Game draw!", font=("Helvetica", 12, "bold"), fill="white")

        # ===================== ROW 1 =====================

        # draw p2 supply
        for i, card in enumerate(self.p2_supply):
            card_image = canvas.create_image(25 + i * 3, 50 - i * 3, image=card_images[red_reverse_path], anchor=tk.NW)

        # label
        if len(self.p2_supply) > 0:
            self.canvas.create_text(90, 240, text=("player 2 supply: " + str(len(self.p2_supply))),
                                    font=("Fixedsys", 8), fill="white")

        # draw p2 hand
        for i, card in enumerate(self.p2_hand):
            image_path = self.p2_hand[i].get_image_path()
            card_image = canvas.create_image(225 + i * 140, 50, image=card_images[image_path], anchor=tk.NW)

        # label
        self.canvas.create_text(565, 25, text="player 2 hand", font=("Fixedsys", 8), fill="white")

        # ===================== ROW 2 =====================

        # draw p2 reshuffle stack
        for i, card in enumerate(self.p1_reshuffle):
            card_image = canvas.create_image(225 + i * 3, 300 - i * 3, image=card_images[red_reverse_path],
                                             anchor=tk.NW)

        # label
        if len(self.p2_reshuffle) > 0:
            self.canvas.create_text(290, 490, text=("reshuffle: " + str(len(self.p2_reshuffle))), font=("Fixedsys", 8),
                                    fill="white")

        # draw gamestack 1
        for i, card in enumerate(self.gamestack1):
            image_path = self.gamestack1[i].get_image_path()
            card_image = canvas.create_image(430 - i * 2, 300 - i * 2, image=card_images[image_path], anchor=tk.NW)
            # add only the top card to the clickable list with corresponding event
            if i == len(self.gamestack1) - 1:
                self.clickable_items[card_image] = ClickEvent("PUT CARD", 1)
                # highlight the gamestack if a card is chosen
                # if self.chosen_card is not None:
                #     highlight_rect = canvas.create_rectangle(0, 0, 0, 0, outline='lightblue', width=3, state='normal')
                #     canvas.coords(highlight_rect, canvas.bbox(card_image))



        # draw gamestack 2
        for i, card in enumerate(self.gamestack2):
            image_path = self.gamestack2[i].get_image_path()
            card_image = canvas.create_image(580 + i * 2, 300 - i * 2, image=card_images[image_path], anchor=tk.NW)
            # add only the top card to the clickable list with corresponding event
            if i == len(self.gamestack2) - 1:
                self.clickable_items[card_image] = ClickEvent("PUT CARD", 2)
                # highlight the gamestack if a card is chosen
                # if self.chosen_card is not None:
                #     highlight_rect = canvas.create_rectangle(0, 0, 0, 0, outline='lightblue', width=3, state='normal')
                #     canvas.coords(highlight_rect, canvas.bbox(card_image))

        # label
        self.canvas.create_text(560, 490, text="game stacks", font=("Fixedsys", 8), fill="white")

        # draw p1 reshuffle stack
        for i, card in enumerate(self.p1_reshuffle):
            card_image = canvas.create_image(785 - i * 3, 300 - i * 3, image=card_images[blue_reverse_path],
                                             anchor=tk.NW)
            # add only the top card to the clickable list with corresponding event
            if i == len(self.p1_reshuffle) - 1:
                self.clickable_items[card_image] = ClickEvent("RESHUFFLE")

        # label
        if len(self.p1_reshuffle) > 0:
            self.canvas.create_text(840, 490, text=("reshuffle: " + str(len(self.p1_reshuffle))), font=("Fixedsys", 8),
                                    fill="white")

        # ===================== ROW 3 =====================

        # draw p1 hand
        for i, card in enumerate(self.p1_hand):
            image_path = self.p1_hand[i].get_image_path()
            card_image = canvas.create_image(225 + i * 140, 530, image=card_images[image_path], anchor=tk.NW)
            # add all cards to the clickable list with corresponding event
            self.clickable_items[card_image] = ClickEvent("CHOOSE CARD", i)

        # label
        self.canvas.create_text(565, 730, text="player 1 hand", font=("Fixedsys", 8), fill="white")

        # draw p1 supply
        for i, card in enumerate(self.p1_supply):
            card_image = canvas.create_image(975 - i * 3, 530 - i * 3, image=card_images[blue_reverse_path],
                                             anchor=tk.NW)
            # add only the top card to the clickable list with corresponding event
            if i == len(self.p1_supply) - 1:
                self.clickable_items[card_image] = ClickEvent("DRAW CARD")

        # label
        if len(self.p1_supply) > 0:
            self.canvas.create_text(1030, 720, text=("player 1 supply: " + str(len(self.p1_supply))),
                                    font=("Fixedsys", 8), fill="white")

    # ===================== GUI event handlers ====================
    def notify(self, event):
        pass

    def repaint(self):
        self.root.after(0, self.repaint_canvas)

    def reshuffle_call(self):
        self.game_state = GameState.WAITING_FOR_RESHUFFLE
        self.repaint()

    def reshuffle_done(self):
        self.game_state = GameState.GAME_IN_PROGRESS
        self.repaint()

    def player_1_wins(self):
        self.game_state = GameState.PLAYER_1_WINS
        self.clickable_items.clear()
        self.repaint()
        self.clickable_items.clear()

    def player_2_wins(self):
        self.game_state = GameState.PLAYER_2_WINS
        self.clickable_items.clear()
        self.repaint()
        self.clickable_items.clear()

    def game_draw(self):
        self.game_state = GameState.GAME_DRAW
        self.clickable_items.clear()
        self.repaint()
        self.clickable_items.clear()

    def repaint_canvas(self):
        # clear everything and recreate
        self.canvas.delete("all")
        self.clickable_items.clear()
        self.draw_gameboard(self.canvas, self.card_images)
        self.create_clickable_highlight_rect()
        self.create_chosen_highlight_rect()
        self.highlight_chosen_card(self.canvas, self.chosen_card)
        self.canvas.tag_raise(self.chosen_highlight_rect)

