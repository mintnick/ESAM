from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import os
from os.path import isfile
import files

# main window components
root = Tk() # main window
title = 'ESAM' # title
icon = 'images' + os.sep + 'icon.ico' # icon
size = '800x600+400+400' # size
serenity_btn = Button() # serenity button
tranquility_btn = Button() # tranquility button
path_box = ttk.Combobox() # path box
selected_path = StringVar(root) # path string
open_btn = Button() # open-selected-dir button
refresh_btn = Button() # refresh-files button
character_box = ttk.Treeview() # characters box
account_box = ttk.Treeview() # accounts box
overwrite_btn = Button() # overwrite button
help_btn = Button() # help button

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
    path_box = ttk.Combobox(root, state='readonly', textvariable=selected_path)
    path_box.place(relx=path_box_start, rely=path_box_top, relwidth=path_box_width, relheight=path_box_height)

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
    character_box_columns = ('角色ID', '角色名')
    character_box = ttk.Treeview(root, columns=character_box_columns, show='headings')
    character_box.place(relx=0.02, rely=character_box_top, relwidth=character_box_width, relheight=character_box_height)

    # accounts box
    account_box_label_top = char_box_label_top
    account_box_label = Label(root, text='账号', font=char_box_label_font)
    account_box_label.place(relx=0.7, rely=account_box_label_top)

    account_box_top = account_box_label_top + 0.05
    account_box_width = character_box_width
    account_box_height = character_box_height
    account_box_columns = ('账号ID', '最后修改时间')
    account_box = ttk.Treeview(root, columns=account_box_columns, show='headings')
    account_box.place(relx=0.52, rely=account_box_top, relwidth=account_box_width, relheight=character_box_height)

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
    help_btn_font = ('bold', 20)
    help_btn = Button(root, text='使用说明', font=help_btn_font, command=open_help)
    help_btn.place(relx=help_btn_start, rely=help_btn_top, relwidth=help_btn_width, relheight=help_btn_height)

# Change server
# TODO:change button color, change default path, change boxes content
def change_server(server):
    fileReader.server = server

# Change setting files path
# TODO: change path box, change boxes content
def change_path():
    current_directory = filedialog.askdirectory(
        parent=root,
        initialdir=fileReader.root,
        title='选择包含设置文件的文件夹'
    )

# Open selected directory
# TODO: open directory
def open_dir():
    os.system('explorer.exe' + selected_path)

# Refresh files
# TODO: refresh
def refresh_files():
    print('')

# Overwrite files
# TODO: overwrite
def overwrite():
    print('')

# Open help window
def open_help():
    print('')

createGUI()
root.mainloop()