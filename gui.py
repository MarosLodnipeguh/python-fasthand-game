import os
import tkinter as tk
from PIL import Image, ImageTk
from logic import GameLogic


class GameGUI:

    # Constants for grid layout
    ROWS = 4
    COLUMNS = 10
    CARD_WIDTH = 120  # Adjust based on your card image dimensions
    CARD_HEIGHT = 180  # Adjust based on your card image dimensions
    SCREEN_WIDTH = COLUMNS * CARD_WIDTH
    SCREEN_HEIGHT = ROWS * CARD_HEIGHT
    PADDING_X = 10
    PADDING_Y = 10

    canvas = None
    card_images = []
    clickable_items = []
    highlight_rect = None

    # shared lists
    p1_hand = []
    p1_supply = []
    p1_reshuffle = []
    p2_hand = []
    p2_supply = []
    p2_reshuffle = []
    gamestack1 = []
    gamestack2 = []
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Card Game")

        self.logic = None

        # UI components

        # Create a canvas to display cards
        self.canvas = tk.Canvas(self.root, width=self.SCREEN_WIDTH, height=self.SCREEN_HEIGHT, bg='green')
        self.canvas.pack()

        # start_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        # start_button.pack()
        #
        # self.label = tk.Label(self.root, text="Game not started")
        # self.label.pack()

        self.load_card_images()

        # Create a highlight rectangle (initially hidden)
        self.highlight_rect = self.canvas.create_rectangle(0, 0, 0, 0, outline='yellow', width=3, state='hidden')

        # Bind mouse motion to the on_mouse_move function
        self.canvas.bind('<Motion>', self.on_mouse_move)
        self.canvas.bind('<Button-1>', self.on_click)

        # ===================== End of constructor =====================

    def set_logic(self, logic):
        self.logic = logic

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
        file_list = self.get_all_files(folder_path)
        # scale the images to the same size
        for path in file_list:
            image = Image.open(path)
            image = image.resize((self.CARD_WIDTH, self.CARD_HEIGHT))  # Resize the image to 100x100 pixels
            photo = ImageTk.PhotoImage(image)
            self.card_images.append(photo)

    def get_all_files(self, folder_path):
        # List all files in the specified directory
        filenames = os.listdir(folder_path)
        # Filter out directories and include the full path for files
        filepaths = [os.path.join(folder_path, f) for f in filenames if os.path.isfile(os.path.join(folder_path, f))]
        return filepaths

    def start_game(self):
        pass

    def update(self):
        print("Updating GUI")
        # self.canvas.delete("all")  # "all" is a special tag to delete all items
        # self.hover_highlight_items.clear()
        self.draw_gameboard()

    def run(self):
        self.root.mainloop()

    # Function to handle card highlight on mouse move
    def on_mouse_move(self, event):
        canvas = self.canvas  # Alias for self.canvas
        highlight_rect = self.highlight_rect  # Alias for self.highlight_id

        for card_id in self.clickable_items:
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
        canvas = self.canvas

        for card_id in self.clickable_items:
            bbox = canvas.bbox(card_id)
            if bbox and bbox[0] <= event.x <= bbox[2] and bbox[1] <= event.y <= bbox[3]:
                self.image_click_function(card_id)
                break

    def image_click_function(self, image_id):
        print(f"Image {image_id} clicked!")


    def draw_gameboard(self):
        canvas = self.canvas  # Alias for self.canvas
        card_images = self.card_images  # Alias for self.card_images

        # ===================== ROW 1 =

        # draw p2 supply
        for i, card in enumerate(self.p2_supply):
            card_id = canvas.create_image(100 + i * 3, 100 - i * 3, image=card_images[1], anchor=tk.NW)

        # draw p2 hand
        for i, card in enumerate(self.p2_hand):
            card_id = canvas.create_image(300 + i * 140, 100, image=card_images[1], anchor=tk.NW)

        # ===================== ROW 2

        # draw p2 reshuffle stack
        for i, card in enumerate(self.p1_reshuffle):
            card_id = canvas.create_image(100 + i * 3, 300 - i * 3, image=card_images[1], anchor=tk.NW)

        # draw gamestacks
        canvas.create_image(450, 300, image=card_images[20], anchor=tk.NW)
        canvas.create_image(600, 300, image=card_images[40], anchor=tk.NW)

        # draw p1 reshuffle stack
        for i, card in enumerate(self.p1_reshuffle):
            card_id = canvas.create_image(1000 + i * 5, 300 - i * 5, image=card_images[0], anchor=tk.NW)

        # ===================== ROW 3

        # draw p1 hand
        for i, card in enumerate(self.p1_hand):
            card_id = canvas.create_image(150 + i * 140, 500, image=card_images[i + 2], anchor=tk.NW)
            self.clickable_items.append(card_id)

        # draw p1 supply
        for i, card in enumerate(self.p1_supply):
            card_id = canvas.create_image(900 + i * 3, 500 - i * 3, image=card_images[0], anchor=tk.NW)
            # add the last card to the highlight list
            last_item_index = -1
            if len(self.p1_supply) > 0:
                last_item_index = len(self.p1_supply) - 1
            if i == last_item_index:
                self.clickable_items.append(card_id)

