import os
import tkinter as tk
from PIL import Image, ImageTk

# Constants for grid layout
ROWS = 4
COLUMNS = 10
CARD_WIDTH = 120  # Adjust based on your card image dimensions
CARD_HEIGHT = 180  # Adjust based on your card image dimensions
SCREEN_WIDTH = COLUMNS * CARD_WIDTH
SCREEN_HEIGHT = ROWS * CARD_HEIGHT
PADDING_X = 10
PADDING_Y = 10

# Function to handle mouse movement
def on_mouse_move(event):
    for card_id in card_ids:
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
folder_path = 'images'
file_list = get_all_files(folder_path)
card_images = []
# scale the images to the same size
for path in file_list:
    image = Image.open(path)
    image = image.resize((CARD_WIDTH, CARD_HEIGHT))  # Resize the image to 100x100 pixels
    photo = ImageTk.PhotoImage(image)
    card_images.append(photo)

# draw a stack
cars_stack_ids = []
for i in range(7):
    card_id = canvas.create_image(150 + i * 5, 100 - i*5, image=card_images[0], anchor=tk.NW)
    cars_stack_ids.append(card_id)

# Draw cards on the canvas
card_ids = []
for i in range(5):
    card_id = canvas.create_image(150 + i * 150, 500, image=card_images[i], anchor=tk.NW)
    card_ids.append(card_id)

# for i, img in enumerate(card_images):
#     card_id = canvas.create_image(100 + (i % 10) * 80, 100 + (i // 10) * 120, image=img, anchor=tk.NW)
#     card_ids.append(card_id)

# Create a highlight rectangle (initially hidden)
highlight_id = canvas.create_rectangle(0, 0, 0, 0, outline='yellow', width=3, state='hidden')

# Bind mouse motion to the on_mouse_move function
canvas.bind('<Motion>', on_mouse_move)

# Start the Tkinter main loop
root.mainloop()
