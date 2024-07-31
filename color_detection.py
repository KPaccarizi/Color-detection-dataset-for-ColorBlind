import cv2
import numpy as np
import pandas as pd
from tkinter import filedialog, Tk, Label, Button, Frame, messagebox

# Initialize global variables
clicked = False
r = g = b = xpos = ypos = 0
img = None

# Load the color names and values from the CSV file
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

# Function to calculate the color name from RGB values
def getColorName(R, G, B):
    minimum = 10000
    cname = "Unknown"
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d < minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

# Function to handle mouse events and get the color of the clicked pixel
def draw_function(event, x, y, flags, param):
    global b, g, r, xpos, ypos, clicked, img
    if event == cv2.EVENT_LBUTTONDBLCLK:
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

# Function to open file dialog and select an image file
def open_image():
    global img, window
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    try:
        img = cv2.imread(file_path)
        if img is None:
            raise ValueError("Invalid image file")
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', draw_function)
        window.after(100, update_image)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to update the image window
def update_image():
    global clicked, img, window
    if clicked:
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)
        text = getColorName(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
        clicked = False

    cv2.imshow("image", img)
    if cv2.getWindowProperty('image', cv2.WND_PROP_VISIBLE) < 1:
        cv2.destroyAllWindows()
        window.quit()  # Stop the Tkinter main loop
        return

    window.after(100, update_image)

# Function to handle Tkinter window close event
def on_closing():
    global window
    cv2.destroyAllWindows()
    window.quit()

# Create the main window
window = Tk()
window.title("Color Detection for Color Blindness")
window.geometry("400x300")

# Bind the window close event
window.protocol("WM_DELETE_WINDOW", on_closing)

# Create and place the widgets
frame = Frame(window, padx=10, pady=10)
frame.pack(expand=True, fill='both')

label = Label(frame, text="Color Detection for Color Blindness", font=("Helvetica", 16))
label.pack(pady=10)

open_button = Button(frame, text="Open Image", command=open_image, font=("Helvetica", 12))
open_button.pack(pady=10)

info_label = Label(frame, text="Double-click on the image to detect color", font=("Helvetica", 10))
info_label.pack(pady=10)

# Start the main loop
window.mainloop()
