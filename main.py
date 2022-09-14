from tkinter import *
from PIL import Image, ImageTk
from screenshot import screenshot
from pytesseract import pytesseract, image_to_string

pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def parse_string(string):
    raw_char = string[0].upper()

    if raw_char == '|':
        raw_char = 'I'
    
    return raw_char

def parse_table(image):
    grid = [[None for i in range(4)] for i in range(4)]

    for i in range(4):
        for j in range(4):
            crop = image.crop((55 + i*125, 370 + j*125, 115 + i*125, 430 + j*125))
            crop.save(f'img/cell_{i}_{j}.png')

            config = r'-l eng --oem 3 --psm 10'
            grid[i][j] = parse_string(image_to_string(crop, config=config))
    
    return grid

def save_image():
    # print('hai')
    global image
    # image = Image.open('img/test.png')
    image = screenshot('BlueStacks App Player')
    pi = ImageTk.PhotoImage(image)

    global label
    label.configure(image=pi)

    global grid
    grid = parse_table(image)

image = None

window = Tk('remote')
window.lift()
window.attributes('-topmost',True)
window.geometry("500x1000")

capture = Button(window, text='capture', command=save_image)
capture.pack()

label = Label(window, image=image)
label.pack()

window.mainloop()

# 60, 370 - 120, 430  -> 240

