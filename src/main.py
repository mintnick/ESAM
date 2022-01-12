from tkinter import *
from tkinter import filedialog
import os
from os.path import isfile
import files

# main window
root = Tk()
title = 'ESAM'
icon = 'images' + os.sep + 'icon.ico'
size = '800x600+400+400'
serenity_btn = Button()
tranquility_btn = Button()
selected_path = StringVar(root)

# file reader
fileReader = files.SettingFilesReader('Serenity')

# render GUI
def createGUI():
    root.title(title)
    if isfile(icon):
        root.iconbitmap(icon)
    root.geometry(size)
    root.resizable(0, 0)

    # top buttons
    serenity_btn = Button(text='国服',font=('bold', 25), command=lambda: change_server('Serenity'))
    serenity_btn.place(relx=0.25, rely=0.02, relwidth=0.15, height=50)
    tranquility_btn = Button(text='欧服',font=('bold', 25), command=lambda: change_server('Tranquility'))
    tranquility_btn.place(relx=0.6, rely=0.02, relwidth=0.15, height=50)

    # path box
    selected_path = 'hello'
    path_box = Entry(root, textvariable=selected_path)
    path_box.place(relx=0.05, rely=0.12, relwidth=0.8, height=30)

    # path buttons
    change_path_btn = Button(root, text='修改路径', command=change_path)
    change_path_btn.place(relx=0.85, rely=0.12, relwidth=0.1, height=30)

# Change server
def change_server(server):
    fileReader.server = server

# Change setting files path
def change_path():
    current_directory = filedialog.askdirectory(
        parent=root,
        initialdir=fileReader.root,
        title='选择包含设置文件的文件夹'
    )

createGUI()
root.mainloop()