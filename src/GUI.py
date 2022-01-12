from tkinter import *
import os
from os.path import isfile

class GUI:
    title = 'ESAM'
    icon = 'images' + os.sep + 'icon.ico'
    size = '800x800+400+400'

    def __init__(self):
        window = Tk()
        window.title(self.title)
        if isfile(self.icon):
            window.iconbitmap(self.icon)
        window.geometry(self.size)

        # top buttons
        serenity_btn = Button(text='国服',font=('bold', 25), command=())
        serenity_btn.place(relx=0.2, rely=0.02, relwidth=0.15, height=50)
        tranquility_btn = Button(text='欧服',font=('bold', 25), command=())
        tranquility_btn.place(relx=0.65, rely=0.02, relwidth=0.15, height=50)

        window.mainloop()

gui = GUI()