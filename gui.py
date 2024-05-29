import os
import sys
import tkinter as tk
from PIL import Image, ImageTk
from threading import Thread
from models.game_event import ClickEvent


class GameGUI:
    # Constants for layout
    # ROWS = 4
    # COLUMNS = 10
    CARD_WIDTH = 120  # Adjust based on your card image dimensions
    CARD_HEIGHT = 180  # Adjust based on your card image dimensions
    # SCREEN_WIDTH = COLUMNS * CARD_WIDTH
    # SCREEN_HEIGHT = ROWS * CARD_HEIGHT
    SCREEN_WIDTH = 1125
    SCREEN_HEIGHT = 750
    # PADDING_X = 10
    # PADDING_Y = 10

    canvas = None
    card_images = {}  # key: image_path, value: photo image object
    clickable_items = {}  # key: card image object (card_id), value: game_event (type of action and card index in its list)
    highlight_rect = None
    bad_highlight_rect = None
    computer_latency = 1
    game_state = "waiting"
    player_chosen_card = None

    # shared lists
    p1_hand = []
    p1_supply = []
    p1_reshuffle = []
    p2_hand = []
    p2_supply = []
    p2_reshuffle = []
    gamestack1 = []
    gamestack2 = []

    def __init__(self, logic):
        self.logic = logic

        self.root = tk.Tk()
        self.root.title("Card Game")

        self.root.protocol("WM_DELETE_WINDOW", self.close_game)

        # UI components

        # Create a canvas to display cards
        self.canvas = tk.Canvas(self.root, width=self.SCREEN_WIDTH, height=self.SCREEN_HEIGHT, bg='green')
        self.canvas.pack()

        button = tk.Button(self.root, text="Start the game", command=self.start_game)
        self.canvas.create_window(600, 300, window=button)

        self.canvas.create_text(600, 365, text="Set the computer latency:", font=("Helvetica", 12, "bold"),
                                fill="white")

        slider = tk.Scale(self.root, from_=0, to=10, orient='horizontal', resolution=0.1,
                          command=self.set_computer_latency)
        self.canvas.create_window(600, 400, window=slider)

        self.load_card_images()

        # Create a highlight rectangle (initially hidden)
        self.create_highlight_rect()

        # Bind mouse motion and click events
        self.canvas.bind('<Motion>', self.on_mouse_move)
        self.canvas.bind('<Button-1>', self.on_click)

    # ===================== End of constructor ====================

    def set_computer_latency(self, value):
        float_value = float(value)
        self.computer_latency = float_value

    def create_highlight_rect(self):
        self.highlight_rect = self.canvas.create_rectangle(0, 0, 0, 0, outline='yellow', width=3, state='hidden')

    def run(self):
        self.root.mainloop()

    def start_game(self):
        self.game_state = "Game in progress"
        # Create and start the game loop thread
        self.game_thread = Thread(target=self.run_game)
        self.game_thread.start()
        self.repaint_canvas()

    def run_game(self):
        self.logic.start_game(self.update_gui, self.computer_latency)

    def update_gui(self, message):
        if message == "reshuffle":
            self.game_state = "Waiting for reshuffle"
            self.canvas.create_text(90, 400, text=self.game_state, font=("Helvetica", 12, "bold"), fill="white")
        elif message == "Player 1 wins":
            self.game_state = "Player 1 wins!"
            self.clickable_items.clear()
            self.canvas.create_text(90, 400, text=self.game_state, font=("Helvetica", 12, "bold"), fill="white")
        elif message == "Player 2 wins":
            self.game_state = "Player 2 wins!"
            self.clickable_items.clear()
            self.canvas.create_text(90, 400, text=self.game_state, font=("Helvetica", 12, "bold"), fill="white")
        elif message == "Game draw":
            self.game_state = "Game draw!"
            self.clickable_items.clear()
            self.canvas.create_text(90, 400, text=self.game_state, font=("Helvetica", 12, "bold"), fill="white")
        elif self.game_state == "Game in progress":
            self.root.after(0, self.repaint_canvas)

    def repaint_canvas(self):
        # clear everything and recreate
        self.canvas.delete("all")  # "all" is a special tag to delete all items
        self.clickable_items.clear()
        self.draw_gameboard()
        self.create_highlight_rect()

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
        folder_path = 'images'
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

    # Function to handle card highlight on mouse move
    def on_mouse_move(self, event):
        canvas = self.canvas  # Alias for self.canvas
        highlight_rect = self.highlight_rect  # Alias for self.highlight_id

        for key in self.clickable_items:
            card_id = key
            # Check if mouse is inside the card's bounding box
            if canvas.bbox(card_id) and canvas.bbox(card_id)[0] <= event.x <= canvas.bbox(card_id)[2] and \
                    canvas.bbox(card_id)[1] <= event.y <= canvas.bbox(card_id)[3]:
                canvas.itemconfig(highlight_rect, state='normal')
                canvas.coords(highlight_rect, canvas.bbox(card_id))
                break
            else:
                canvas.itemconfig(highlight_rect, state='hidden')

    # Function to blink the bad choice rectangle
    def on_bad_mouse_click(self, event):
        pass

    # Function to handle the click event (call the image_click_function when any of clickable items is clicked)
    def on_click(self, event):
        canvas = self.canvas  # Alias for self.canvas
        for key, value in self.clickable_items.items():  # key: card_id, value: game_event
            card_id = key
            bbox = canvas.bbox(card_id)
            if bbox and bbox[0] <= event.x <= bbox[2] and bbox[1] <= event.y <= bbox[3]:
                self.image_click_function(value)
                break

    def image_click_function(self, click_event):
        if click_event.get_name() == "choose card":
            self.player_chosen_card = click_event.get_index()
        elif click_event.get_name() == "put card":
            if self.player_chosen_card is None:
                print("Choose a card first!")
                return
            chosen_gamestack = click_event.get_index()
            self.logic.player_play(self.player_chosen_card, chosen_gamestack, self.update_gui)
            self.player_chosen_card = None
        elif click_event.get_name() == "draw card":
            self.logic.player_draw(self.update_gui)

    def draw_gameboard(self):
        canvas = self.canvas  # Alias for self.canvas
        card_images = self.card_images  # Alias for self.card_images

        blue_reverse_path = "images/0_reverse_blue.png"
        red_reverse_path = "images/0_reverse_red.png"

        # ===================== ROW 1 =====================

        # draw p2 supply
        for i, card in enumerate(self.p2_supply):
            card_id = canvas.create_image(25 + i * 3, 50 - i * 3, image=card_images[red_reverse_path], anchor=tk.NW)

        if len(self.p2_supply) > 0:
            self.canvas.create_text(90, 240, text=("player 2 supply: " + str(len(self.p2_supply))),
                                    font=("Fixedsys", 8), fill="white")

        # draw p2 hand

        # hidden
        # for i, card in enumerate(self.p2_hand):
        #     card_id = canvas.create_image(300 + i * 140, 80, image=card_images[red_reverse_path], anchor=tk.NW)

        # shown
        for i, card in enumerate(self.p2_hand):
            image_path = self.p2_hand[i].get_image_path()
            card_id = canvas.create_image(225 + i * 140, 50, image=card_images[image_path], anchor=tk.NW)

        self.canvas.create_text(565, 25, text="player 2 hand", font=("Fixedsys", 8), fill="white")

        # ===================== ROW 2 =====================

        # draw p2 reshuffle stack
        for i, card in enumerate(self.p1_reshuffle):
            card_id = canvas.create_image(225 + i * 3, 300 - i * 3, image=card_images[red_reverse_path], anchor=tk.NW)

        if len(self.p2_reshuffle) > 0:
            self.canvas.create_text(290, 490, text=("reshuffle: " + str(len(self.p2_reshuffle))), font=("Fixedsys", 8),
                                    fill="white")

        # draw gamestacks
        for i, card in enumerate(self.gamestack1):
            image_path = self.gamestack1[i].get_image_path()
            card_id = canvas.create_image(430 - i * 2, 300 - i * 2, image=card_images[image_path], anchor=tk.NW)
            # add only the last card to the clickable list
            if i == len(self.gamestack1) - 1:
                self.clickable_items[card_id] = ClickEvent("put card", 1)  # Event type: draw card

        for i, card in enumerate(self.gamestack2):
            image_path = self.gamestack2[i].get_image_path()
            card_id = canvas.create_image(580 + i * 2, 300 - i * 2, image=card_images[image_path], anchor=tk.NW)
            # add only the last card to the clickable list
            if i == len(self.gamestack2) - 1:
                self.clickable_items[card_id] = ClickEvent("put card", 2)  # Event type: draw card

        self.canvas.create_text(560, 490, text="game stacks", font=("Fixedsys", 8), fill="white")

        # draw p1 reshuffle stack
        for i, card in enumerate(self.p1_reshuffle):
            card_id = canvas.create_image(785 - i * 3, 300 - i * 3, image=card_images[blue_reverse_path], anchor=tk.NW)

        if len(self.p1_reshuffle) > 0:
            self.canvas.create_text(840, 490, text=("reshuffle: " + str(len(self.p1_reshuffle))), font=("Fixedsys", 8),
                                    fill="white")

        # ===================== ROW 3 =====================

        # draw p1 hand
        for i, card in enumerate(self.p1_hand):
            image_path = self.p1_hand[i].get_image_path()
            card_id = canvas.create_image(225 + i * 140, 530, image=card_images[image_path], anchor=tk.NW)
            self.clickable_items[card_id] = ClickEvent("choose card", i)  # Event type: play card
        self.canvas.create_text(565, 730, text="player 1 hand", font=("Fixedsys", 8), fill="white")

        # draw p1 supply
        for i, card in enumerate(self.p1_supply):
            card_id = canvas.create_image(975 - i * 3, 530 - i * 3, image=card_images[blue_reverse_path], anchor=tk.NW)
            # add only the last card to the clickable list
            if i == len(self.p1_supply) - 1:
                self.clickable_items[card_id] = ClickEvent("draw card", -1)  # Event type: draw card

        if len(self.p1_supply) > 0:
            self.canvas.create_text(1030, 720, text=("player 1 supply: " + str(len(self.p1_supply))), font=("Fixedsys", 8), fill="white")

    def close_game(self):
        self.root.destroy()
        self.logic.close_game()
