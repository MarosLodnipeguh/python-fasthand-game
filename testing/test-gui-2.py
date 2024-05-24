import os
import tkinter as tk
from PIL import Image, ImageTk
# from main import p1_hand, p1_supply, p1_reshuffle, p2_hand, p2_supply, p2_reshuffle, gamestack1, gamestack2

# Constants for grid layout
ROWS = 4
COLUMNS = 10
CARD_WIDTH = 120  # Adjust based on your card image dimensions
CARD_HEIGHT = 180  # Adjust based on your card image dimensions
SCREEN_WIDTH = COLUMNS * CARD_WIDTH
SCREEN_HEIGHT = ROWS * CARD_HEIGHT
PADDING_X = 10
PADDING_Y = 10

hover_highlight_items = []

# Function to handle mouse movement
def on_mouse_move(event):
    for card_id in hover_highlight_items:
        # Check if mouse is inside the card's bounding box
        if canvas.bbox(card_id) and canvas.bbox(card_id)[0] <= event.x <= canvas.bbox(card_id)[2] and canvas.bbox(card_id)[1] <= event.y <= canvas.bbox(card_id)[3]:
            canvas.itemconfig(highlight_id, state='normal')
            canvas.coords(highlight_id, canvas.bbox(card_id))
            break
    else:
        canvas.itemconfig(highlight_id, state='hidden')

# Initialize main window
root = tk.Tk()
root.title("Card Game")

# Create a canvas to display cards
canvas = tk.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg='green')
canvas.pack()

def get_all_files(folder_path):
    # List all files in the specified directory
    filenames = os.listdir(folder_path)
    # Filter out directories and include the full path for files
    filepaths = [os.path.join(folder_path, f) for f in filenames if os.path.isfile(os.path.join(folder_path, f))]
    return filepaths

# Load card images
folder_path = '../images'
file_list = get_all_files(folder_path)
card_images = []
# scale the images to the same size
for path in file_list:
    image = Image.open(path)
    image = image.resize((CARD_WIDTH, CARD_HEIGHT))  # Resize the image to 100x100 pixels
    photo = ImageTk.PhotoImage(image)
    card_images.append(photo)

# ===================== ROW 1 =
# draw p2 supply
p2_supply = []
for i in range(13):
    card_id = canvas.create_image(100 + i * 3, 100 - i*3, image=card_images[1], anchor=tk.NW)
    p2_supply.append(card_id)

# draw p2 hand
p2_hand = []
for i in range(5):
    card_id = canvas.create_image(300 + i * 140, 100, image=card_images[1], anchor=tk.NW)
    p2_hand.append(card_id)

    # ===================== ROW 2

# draw p2 reshuffle stack
p1_reshuffle_stack = []
for i in range(7):
    card_id = canvas.create_image(100 + i * 3, 300 - i*3, image=card_images[1], anchor=tk.NW)
    p1_reshuffle_stack.append(card_id)

    # draw gamestacks
    canvas.create_image(450, 300, image=card_images[20], anchor=tk.NW)
    canvas.create_image(600, 300, image=card_images[40], anchor=tk.NW)

# draw p1 reshuffle stack
p2_reshuffle_stack = []
for i in range(7):
    card_id = canvas.create_image(1000 + i * 5, 300 - i*5, image=card_images[0], anchor=tk.NW)
    p1_reshuffle_stack.append(card_id)

# ===================== ROW 3

# draw p1 hand
p1_hand = []
for i in range(5):
    card_id = canvas.create_image(150 + i * 140, 500, image=card_images[i+2], anchor=tk.NW)
    p1_hand.append(card_id)
    hover_highlight_items.append(card_id)

# draw p1 supply
p1_supply = []
for i in range(13):
    card_id = canvas.create_image(900 + i * 3, 500 - i*3, image=card_images[0], anchor=tk.NW)
    p1_supply.append(card_id)

if len(p1_supply) > 0:
    hover_highlight_items.append(p1_supply[len(p1_supply)-1])

# for i, img in enumerate(card_images):
#     card_id = canvas.create_image(100 + (i % 10) * 80, 100 + (i // 10) * 120, image=img, anchor=tk.NW)
#     card_ids.append(card_id)

# Create a highlight rectangle (initially hidden)
highlight_id = canvas.create_rectangle(0, 0, 0, 0, outline='yellow', width=3, state='hidden')

# Bind mouse motion to the on_mouse_move function
canvas.bind('<Motion>', on_mouse_move)

# Start the Tkinter main loop
root.mainloop()
