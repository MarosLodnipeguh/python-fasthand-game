import os
import tkinter as tk
from PIL import Image, ImageTk
from logic import GameLogic
from threading import Thread
from game_event import GameEvent


class GameGUI:
    # Constants for layout
    ROWS = 4
    COLUMNS = 10
    CARD_WIDTH = 120  # Adjust based on your card image dimensions
    CARD_HEIGHT = 180  # Adjust based on your card image dimensions
    SCREEN_WIDTH = COLUMNS * CARD_WIDTH
    SCREEN_HEIGHT = ROWS * CARD_HEIGHT
    # SCREEN_WIDTH = 1000
    # SCREEN_HEIGHT = 600
    PADDING_X = 10
    PADDING_Y = 10

    canvas = None
    card_images = {} # key: image_path, value: photo
    clickable_items = {}  # key: card image object (card_id), value: game_event (type of action and card index)
    highlight_rect = None
    bad_highlight_rect = None
    computer_latency = 1

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


        # UI components

        # Create a canvas to display cards
        self.canvas = tk.Canvas(self.root, width=self.SCREEN_WIDTH, height=self.SCREEN_HEIGHT, bg='green')
        self.canvas.pack()

        button = tk.Button(self.root, text="Start the game", command=self.start_game)
        self.canvas.create_window(600, 300, window=button)

        # label = tk.Label(self.root, text="Adjust the value:")
        # self.canvas.create_window(200, 200, window=label)  # Position above the slider

        self.canvas.create_text(600, 365, text="Set the computer latency:", font=("Helvetica", 12))

        slider = tk.Scale(self.root, from_=0.5, to=10, orient='horizontal', resolution=0.1, command=self.set_computer_latency)
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
        # Create and start the game loop thread
        self.game_thread = Thread(target=self.run_game)
        # self.game_thread = Thread(target=self.logic.start_game(self.update_gui, self.computer_latency))
        self.game_thread.start()
        self.update_canvas()

    def run_game(self):
        self.logic.start_game(self.update_gui, self.computer_latency)

    def update_gui(self, message):
        # print("logic gui update request with mess: " + message)
        # Update the status label
        # self.root.after(0, lambda: self.game_status.config(text=message))
        # Update the canvas
        self.root.after(0, self.update_canvas)

    def update_canvas(self):
        # print("Updating canvas")
        # clear everything and recreate
        self.canvas.delete("all")  # "all" is a special tag to delete all items
        self.clickable_items.clear()
        self.create_highlight_rect()
        self.draw_gameboard()

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

    # Function to handle the click event
    def on_click(self, event):
        canvas = self.canvas # Alias for self.canvas

        # print(event)
        for key, value in self.clickable_items.items():
            card_id = key
            bbox = canvas.bbox(card_id)
            if bbox and bbox[0] <= event.x <= bbox[2] and bbox[1] <= event.y <= bbox[3]:
                self.image_click_function(value)
                break

    def image_click_function(self, game_event):
        # check if its a play or draw action and call the corresponding logic function
        if game_event.get_type() == "play":
            self.logic.player_play(game_event.get_index(), self.update_gui)
        elif game_event.get_type() == "draw":
            self.logic.player_draw(self.update_gui)


    def draw_gameboard(self):
        canvas = self.canvas  # Alias for self.canvas
        card_images = self.card_images  # Alias for self.card_images

        blue_reverse_path = "images/0_reverse_blue.png"
        red_reverse_path = "images/0_reverse_red.png"

        # ===================== ROW 1 =====================

        # draw p2 supply
        for i, card in enumerate(self.p2_supply):
            card_id = canvas.create_image(100 + i * 3, 80 - i * 3, image=card_images[red_reverse_path], anchor=tk.NW)

        # draw p2 hand
        for i, card in enumerate(self.p2_hand):
            card_id = canvas.create_image(300 + i * 140, 80, image=card_images[red_reverse_path], anchor=tk.NW)

        # ===================== ROW 2 =====================

        # draw p2 reshuffle stack
        for i, card in enumerate(self.p1_reshuffle):
            card_id = canvas.create_image(100 + i * 3, 300 - i * 3, image=card_images[red_reverse_path], anchor=tk.NW)

        # draw gamestacks
        for i, card in enumerate(self.gamestack1):
            image_path = self.gamestack1[i].get_image_path()
            card_id = canvas.create_image(450 - i * 2, 300 - i * 2, image=card_images[image_path], anchor=tk.NW)

        for i, card in enumerate(self.gamestack2):
            image_path = self.gamestack2[i].get_image_path()
            card_id = canvas.create_image(600 + i * 2, 300 - i * 2, image=card_images[image_path], anchor=tk.NW)

        # draw p1 reshuffle stack
        for i, card in enumerate(self.p1_reshuffle):
            card_id = canvas.create_image(1000 - i * 3, 300 - i * 3, image=card_images[blue_reverse_path], anchor=tk.NW)

        # ===================== ROW 3 =====================

        # draw p1 hand
        for i, card in enumerate(self.p1_hand):
            image_path = self.p1_hand[i].get_image_path()
            card_id = canvas.create_image(150 + i * 140, 500, image=card_images[image_path], anchor=tk.NW)
            self.clickable_items[card_id] = GameEvent("play", i)  # Event type: play card

        # draw p1 supply
        for i, card in enumerate(self.p1_supply):
            card_id = canvas.create_image(900 - i * 3, 500 - i * 3, image=card_images[blue_reverse_path], anchor=tk.NW)
            # add the last card to the highlight list
            last_item_index = -1
            if len(self.p1_supply) > 0:
                last_item_index = len(self.p1_supply) - 1
            if i == last_item_index:
                self.clickable_items[card_id] = GameEvent("draw", i)  # Event type: draw card
