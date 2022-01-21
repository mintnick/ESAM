import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import Button
from tkinter import StringVar
from tkinter import Label

import os
from os.path import isfile
import subprocess
import pathlib
import threading

import files
import esi

'''main window components'''
root = tk.Tk() # main window
title = 'ESAM' # title
icon = 'images' + os.sep + 'icon.ico' # icon
size = '700x600+400+400' # size
serenity_btn = Button() # serenity button
tranquility_btn = Button() # tranquility button
path_box = ttk.Combobox(root) # path box
open_btn = Button() # open-selected-dir button
refresh_btn = Button() # refresh-files button
character_box = ttk.Treeview(root) # characters box
account_box = ttk.Treeview(root) # accounts box
overwrite_btn = Button() # overwrite button
help_btn = Button() # help button

'''variables'''
path_list = []  # setting dirs list
selected_path = tk.StringVar() # path string
fileReader = files.SettingFilesReader('Serenity')
characters = []
accounts = []
esi_signal = True # keep reading from esi unless being stopped (change server, dir, etc)

'''render GUI'''
def createGUI():
    root.title(title)
    if isfile(icon):
        root.iconbitmap(icon)
    root.geometry(size)
    root.resizable(0, 0)

    # top buttons
    top_btn_top = 0.01
    top_btn_height = 0.08
    top_btn_1_start = 0.25
    top_btn_2_start = 0.6
    top_btn_width = 0.15
    top_btn_font = ('bold', 25)
    serenity_btn = Button(root, text='国服',font=top_btn_font, command=lambda: change_server('Serenity'))
    serenity_btn.place(relx=top_btn_1_start, rely=top_btn_top, relwidth=top_btn_width, relheight=top_btn_height)
    tranquility_btn = Button(root, text='欧服',font=top_btn_font, command=lambda: change_server('Tranquility'))
    tranquility_btn.place(relx=top_btn_2_start, rely=top_btn_top, relwidth=top_btn_width, relheight=top_btn_height)

    # path box
    path_box_start = 0.01
    path_box_top = 0.11
    path_box_width = 0.98
    path_box_height = 0.05
    selected_path = 'hello'
    path_box['textvariable'] = selected_path
    path_box['state'] = 'readonly'
    path_box.place(relx=path_box_start, rely=path_box_top, relwidth=path_box_width, relheight=path_box_height)
    path_box.bind("<<ComboboxSelected>>", select_path)

    # path buttons
    path_btn_start = 0.13
    path_btn_top = 0.17
    path_btn_width = 0.2
    path_btn_height = 0.07
    path_btn_font = ('bold', 16)
    change_path_btn = Button(root, text='修改路径', font=path_btn_font, command=change_path)
    change_path_btn.place(relx=path_btn_start, rely=path_btn_top, relwidth=path_btn_width, relheight=path_btn_height)

    # open button
    open_btn_start = 0.4
    open_btn_top = path_btn_top
    open_btn_width = path_btn_width
    open_btn_height = path_btn_height
    open_btn = Button(root, text='打开文件夹', font=path_btn_font, command=open_dir)
    open_btn.place(relx=open_btn_start, rely=open_btn_top, relwidth=open_btn_width, relheight=open_btn_height)

    # refresh button
    refresh_btn_start = 0.66
    refresh_btn_top = path_btn_top
    refresh_btn_width = path_btn_width
    refresh_btn_height = path_btn_height
    refresh_btn = Button(root, text='刷新', font=path_btn_font, command=refresh_files)
    refresh_btn.place(relx=refresh_btn_start, rely=refresh_btn_top, relwidth=refresh_btn_width, relheight = refresh_btn_height)

    # separator 1
    separator_1_top = path_btn_top+path_btn_height+0.02
    separator_1 = ttk.Separator(root, orient='horizontal')
    separator_1.place(relx=0, rely=separator_1_top, relwidth=1, relheight=1)

    # characters box
    char_box_label_top = separator_1_top + 0.01
    char_box_label_font = ('bold', 20)
    char_box_label = Label(root, text='角色', font=char_box_label_font)
    char_box_label.place(relx=0.2, rely=char_box_label_top)
    
    character_box_top = char_box_label_top + 0.05
    character_box_width = 0.45
    character_box_height = 0.55

    column_1_width = int(700*character_box_width*0.4)
    column_2_width = int(700*character_box_width*0.6)

    global character_box
    character_box = ttk.Treeview(root, columns=('character_id', 'character_name'), show='headings')
    character_box.heading('character_id', text='角色ID')
    character_box.column('character_id', width=column_1_width, minwidth=column_1_width, anchor=tk.CENTER, stretch=False)
    character_box.heading('character_name', text='角色名')
    character_box.column('character_name', width=column_2_width, minwidth=column_2_width, anchor=tk.CENTER, stretch=False)
    character_box.place(relx=0.02, rely=character_box_top, relwidth=character_box_width, relheight=character_box_height)
    character_scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=character_box.yview)
    character_box.configure(yscroll=character_scrollbar.set)
    character_scrollbar.place(relx=0.47, rely=character_box_top, relheight=character_box_height)

    # accounts box
    account_box_label_top = char_box_label_top
    account_box_label = Label(root, text='账号', font=char_box_label_font)
    account_box_label.place(relx=0.7, rely=account_box_label_top)

    account_box_top = account_box_label_top + 0.05
    account_box_width = character_box_width
    account_box_height = character_box_height
    account_box_columns = ('account_id', 'last_mod_time')
    global account_box
    account_box = ttk.Treeview(root, columns=account_box_columns, show='headings', height=10)
    account_box.heading('account_id', text='账号ID')
    account_box.column('account_id', width=column_1_width, minwidth=column_1_width, anchor=tk.CENTER, stretch=False)
    account_box.heading('last_mod_time', text='最后修改时间')
    account_box.column('last_mod_time', width=column_2_width, minwidth=column_2_width, anchor=tk.CENTER, stretch=False)
    account_box.place(relx=0.52, rely=account_box_top, relwidth=account_box_width, relheight=character_box_height)
    account_scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=account_box.yview)
    account_box.configure(yscroll=account_scrollbar.set)
    account_scrollbar.place(relx=0.97, rely=account_box_top, relheight=account_box_height)

    # separator 2
    separator_2_top = character_box_top + character_box_height + 0.02
    separator_2 = ttk.Separator(root, orient='horizontal')
    separator_2.place(relx=0, rely=separator_2_top, relwidth=1, relheight=1)

    # overwrite button
    overwrite_btn_start = 0.3
    overwrite_btn_top = separator_2_top + 0.02
    overwrite_btn_width = 0.4
    overwrite_btn_height = 0.07
    overwrite_btn_font = ('bold', 25)
    overwrite_btn = Button(root, text='确认覆盖', font=overwrite_btn_font, command=overwrite)
    overwrite_btn.place(relx=overwrite_btn_start, rely=overwrite_btn_top, relwidth=overwrite_btn_width, relheight=overwrite_btn_height)

    # help_btn
    help_btn_start = 0.8
    help_btn_top = overwrite_btn_top
    help_btn_width = 0.15
    help_btn_height = 0.07
    help_btn_font = ('bold', 16)
    help_btn = Button(root, text='使用说明', font=help_btn_font, command=open_help)
    help_btn.place(relx=help_btn_start, rely=help_btn_top, relwidth=help_btn_width, relheight=help_btn_height)

''' Change server '''
def change_server(server):
    fileReader.server = server
    read_dirs()
    refresh_files()

''' Select path '''
def select_path(event):
    selected_path.set(event.widget.get())
    refresh_files()

'''Change setting files path'''
def change_path():
    current_directory = filedialog.askdirectory(
        parent=root,
        initialdir=fileReader.root,
        title='选择包含设置文件的文件夹'
    )
    current_directory = pathlib.PureWindowsPath(current_directory)
    selected_path.set(current_directory)
    path_box.set(selected_path.get())
    refresh_files()

'''Open selected directory'''
def open_dir():
    if not os.path.isdir(selected_path.get()):
        return
    os.startfile(selected_path.get())

'''Refresh files'''
def refresh_files():
    character_box.delete(*character_box.get_children())
    account_box.delete(*account_box.get_children())
    characters = []
    accounts = []
    esi_signal = True

    characters = fileReader.read_character(selected_path.get())
    accounts = fileReader.read_account(selected_path.get())

    for c in characters:
        character_box.insert('', tk.END, values=(c[0], c[1]))
    for a in accounts:
        account_box.insert('', tk.END, values=a)

    # TODO: read name in backend thread, edit treeview rows
    while esi_signal == True and characters:
        esiReader = esi.EsiReader(fileReader.server)
        for c in characters:
            c_name = esiReader.get_character_name(c[0])
            if c_name == '':
                c_name = '未知'
            print(c_name)
        esi_signal = False

'''Overwrite files'''
# TODO: overwrite
def overwrite():
    print('')

'''Open help window'''
# TODO: write help msg, open help window
def open_help():
    print('')

'''Read dirs'''
def read_dirs():
    path_list = fileReader.getDirs()
    path_box['values'] = path_list
    selected_path.set(path_list[0])
    path_box.set(selected_path.get())

createGUI()
read_dirs()
refresh_files()
root.mainloop()