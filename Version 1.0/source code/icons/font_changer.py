from tkinter import font
from tkinter import *

root = Tk()
root.title("Font Changer")
root.geometry("500x500")

fonts = font.families()

pos = 0
def next_font():
    global fonts, pos
    pos += 1
    if pos >= len(fonts):
        pos = 0
    Label(root, text=fonts[pos], font=fonts[pos]).pack()

def prev_font():
    global fonts, pos
    if pos == 0:
        pos = len(fonts) - 1
    Label(root, text=fonts[pos], font=fonts[pos]).pack()

Button(root, text="Previous", command=prev_font()).pack(side='right')
Button(root, text="Next", command=next_font()).pack(side='left')




root.mainloop()