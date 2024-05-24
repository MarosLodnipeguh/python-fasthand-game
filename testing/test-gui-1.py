# test-gui-1.py
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from logic import init_new_game, player_turn, computer_turn, print_game_table  # Importuj logikę gry

from logic import p1_hand, p1_supply, p1_reshuffle, p2_hand, p2_supply, p2_reshuffle, gamestack1, gamestack2

folder_path = '../images'
ROWS = 4
COLUMNS = 13
CARD_WIDTH = 72  # Adjust based on your card image dimensions
CARD_HEIGHT = 96  # Adjust based on your card image dimensions
PADDING_X = 10
PADDING_Y = 10
# scaled_images = []

def get_all_files(folder_path):
    # List all files in the specified directory
    filenames = os.listdir(folder_path)
    # Filter out directories and include the full path for files
    filepaths = [os.path.join(folder_path, f) for f in filenames if os.path.isfile(os.path.join(folder_path, f))]
    return filepaths

# Function to handle mouse movement
# def on_mouse_move(event):
#     for card_id in card_ids:
#         # Check if mouse is inside the card's bounding box
#         if canvas.bbox(card_id) and canvas.bbox(card_id)[0] <= event.x <= canvas.bbox(card_id)[2] and canvas.bbox(card_id)[1] <= event.y <= canvas.bbox(card_id)[3]:
#             canvas.itemconfig(highlight_id, state='normal')
#             canvas.coords(highlight_id, canvas.bbox(card_id))
#             break
#     else:
#         canvas.itemconfig(highlight_id, state='hidden')

class CardGameGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Fast Hand card game")

        # load all images from the images folder

        file_list = get_all_files(folder_path)
        # print(file_list)

        # scale the images to the same size
        self.scaled_images = []
        for path in file_list:
            image = Image.open(path)
            image = image.resize((150, 250))  # Resize the image to 100x100 pixels
            photo = ImageTk.PhotoImage(image)
            self.scaled_images.append(photo)

        # Tworzenie przycisków i etykiet
        self.init_widgets()

        # Inicjalizacja gry
        # self.new_game()


    def init_widgets(self):
        canvas = tk.Canvas(root, width=800, height=600, bg='green')
        canvas.pack()

        # Etykiety do wyświetlania informacji o kartach


        player1_hand_labels = []
        player2_hand_labels = []


        # Player 2 Hand
        for i in range(5):
            player2_hand_labels.append(tk.Label(self.root, image=self.scaled_images[1]))
            player2_hand_labels[i].grid(row=0, column=i, padx=5, pady=5)
        # Player 2 Supply
        self.p2_supply_label = tk.Label(self.root, text="Player 2 Supply: ")
        self.p2_supply_label.grid(row=0, column=5, padx=5, pady=5)



        # Gamestacks & Reshuffles
        reshuffle1_image = tk.Label(self.root, image=self.scaled_images[1])
        reshuffle1_image.grid(row=1, column=0, padx=5, pady=5)
        reshuffle1_text = tk.Label(self.root, text="Enemy Reshuffle: 7")
        reshuffle1_text.grid(row=1, column=1, padx=5, pady=5)

        gamestack1_image = tk.Label(self.root, image=self.scaled_images[2])
        gamestack1_image.grid(row=1, column=3, padx=5, pady=5)

        gamestack2_image = tk.Label(self.root, image=self.scaled_images[3])
        gamestack2_image.grid(row=1, column=4, padx=5, pady=5)

        reshuffle2_text = tk.Label(self.root, text="Your Reshuffle : 69")
        reshuffle2_text.grid(row=1, column=6, padx=5, pady=5)
        reshuffle2_image = tk.Label(self.root, image=self.scaled_images[0])
        reshuffle2_image.grid(row=1, column=7, padx=5, pady=5)

        # Player 1 Hand
        for i in range(5):
            player1_hand_labels.append(tk.Label(self.root, image=self.scaled_images[i]))
            player1_hand_labels[i].grid(row=3, column=i, padx=5, pady=5)  # Place labels in a row
            # player1_hand_labels[i].pack()
        # Player 1 Supply
        self.p1_supply_label = tk.Label(self.root, text="Player 1 Supply: ")
        self.p1_supply_label.grid(row=3, column=5, padx=5, pady=5)


        # self.gamestack1_label = tk.Label(self.root, image=self.scaled_images[0])
        # self.gamestack1_label.pack()

        # Define a function to handle the click event
        # def on_image_click(event):
        #     print("Image clicked!")
        #
        # # Bind the click event to the Label widget
        # self.gamestack1_label.bind("<Button-1>", on_image_click)
        #





        # self.p2_hand_label = tk.Label(self.root, text="Player 2 Hand: ")
        # self.p2_hand_label.pack()
        #
        # # self.gamestack1_label = tk.Label(self.root, text="Gamestack 1: ")
        # # self.gamestack1_label.pack()
        #
        # self.gamestack2_label = tk.Label(self.root, text="Gamestack 2: ")
        # self.gamestack2_label.pack()
        #
        # # Przycisk nowej gry
        # self.new_game_button = tk.Button(self.root, text="New Game", command=self.new_game)
        # self.new_game_button.pack()
        #
        # # Przycisk ruchu gracza 1
        # self.player1_turn_button = tk.Button(self.root, text="Player 1 Turn", command=self.player1_turn)
        # self.player1_turn_button.pack()

    def new_game(self):
        init_new_game()
        self.update_display()

    def player1_turn(self):
        if player_turn(p1_hand, p1_supply):
            self.update_display()
            self.computer_turn()
        else:
            messagebox.showinfo("Info", "Player 1 cannot play any card.")

    def computer_turn(self):
        if computer_turn(p2_hand, p2_supply):
            self.update_display()
        else:
            messagebox.showinfo("Info", "Computer cannot play any card.")

    def update_display(self):
        self.p1_hand_label.config(text=f"Player 1 Hand: {p1_hand}")
        self.p2_hand_label.config(text=f"Player 2 Hand: {p2_hand}")
        self.gamestack1_label.config(text=f"Gamestack 1: {gamestack1[0]}")
        self.gamestack2_label.config(text=f"Gamestack 2: {gamestack2[0]}")

        # Sprawdzanie wygranej
        if len(p1_hand) == 0 and len(p1_supply) == 0:
            messagebox.showinfo("Info", "Player 1 won the game!")
        if len(p2_hand) == 0 and len(p2_supply) == 0:
            messagebox.showinfo("Info", "Player 2 won the game!")


if __name__ == "__main__":
    root = tk.Tk()
    app = CardGameGUI(root)
    root.mainloop()
