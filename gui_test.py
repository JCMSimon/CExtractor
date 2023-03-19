import tkinter as tk
from PIL import Image,ImageTk

# Create the main window
root = tk.Tk()

# Set the title of the window
root.title("My GUI")

# Add a label for the text
label = tk.Label(root, text="My Text")
label.pack()

# Create a frame for the buttons
frame = tk.Frame(root)

# Add images to the buttons

image1 = ImageTk.PhotoImage(Image.open("48101output.png"))
button1 = tk.Checkbutton(frame, image=image1)

image2 = ImageTk.PhotoImage(Image.open("48101output.png"))
button2 = tk.Checkbutton(frame, image=image2)

image3 = ImageTk.PhotoImage(Image.open("48101output.png"))
button3 = tk.Checkbutton(frame, image=image3)

tk.

# Pack the buttons into the frame in a grid layout
button1.grid(row=0, column=0)
button2.grid(row=0, column=1)
button3.grid(row=0, column=2)
frame.pack()

# Add a submit button
submit_button = tk.Button(root, text="Submit")
submit_button.pack()

# Start the main event loop
root.mainloop()