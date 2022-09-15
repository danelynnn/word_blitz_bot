from tkinter import *
from PIL import Image, ImageTk
from screenshot import screenshot
from pytesseract import pytesseract, image_to_string
from algorithm import find_solutions, trie
from win32 import win32gui
import ctypes
import time

pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def parse_string(string):
    raw_char = string[0].lower()

    if raw_char == '|':
        raw_char = 'i'
    
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

def execute_path(path, window_loc):
    hwnd = win32gui.FindWindow(None, 'BlueStacks App Player')
    win32gui.SetForegroundWindow(hwnd)
    
    start = path[0]
    ctypes.windll.user32.SetCursorPos(window_loc[0] + 70 + start[0]*125, window_loc[1] + 385 + start[1]*125)
    ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
    time.sleep(0.05)

    for pos in path[1:]:
        ctypes.windll.user32.SetCursorPos(window_loc[0] + 70 + pos[0]*125, window_loc[1] + 385 + pos[1]*125)
        time.sleep(0.05)
    
    ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)
    print(f'executing {path}')

def save_image():
    # print('hai')
    global image
    image, position = screenshot('BlueStacks App Player')
    pi = ImageTk.PhotoImage(image)
    image.save('img/test.png')
    # image = Image.open('img/test.png')

    # global label
    # label.configure(image=pi)

    global grid
    grid = parse_table(image)

    print(grid)

    words_list = find_solutions(grid)

    global solutions
    index = 0
    longest_words = sorted(list(words_list.keys()), key=len, reverse=True)
    for word in longest_words:
        Button(solutions, text=word, command=(lambda i=words_list[word]: execute_path(i, position))).grid(row=index, column=0)
        label = Label(solutions, text=words_list[word])
        label.grid(row=index, column=1)

        index += 1

    for i in range(250):
        execute_path(words_list[longest_words[i]], position)
        time.sleep(0.05)

    # print(words_list)

image = None

window = Tk('remote')
window.lift()
window.attributes('-topmost',True)
window.geometry("500x1000")

capture = Button(window, text='capture', command=save_image)
capture.pack()
button = Button(window, text='test button', command=(lambda: execute_path([[0, 0], [1, 0], [1, 1]], (1326, 9))))
button.pack()

# label = Label(window, image=image)
# label.pack()

solutions = Frame(window)
solutions.pack()

window.mainloop()



# 60, 370 - 120, 430  -> 240

