import tkinter as tk
from PIL import Image, ImageTk

# Create a Tkinter window
window = tk.Tk()
window.title("Image Viewer")

# Path to the JPEG image file
image_file = "book_pics/1984.jpg"

# Open the JPEG image file using PIL
image = Image.open(image_file)

# Convert the image to a Tkinter-compatible format
tk_image = ImageTk.PhotoImage(image)

# Create a Tkinter label to display the image
label = tk.Label(window, image=tk_image)
label.pack()

# Run the Tkinter event loop
window.mainloop()
