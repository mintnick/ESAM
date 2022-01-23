import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import Button
from tkinter import StringVar
from tkinter import Label
from tkinter import messagebox

import os
from os.path import isfile
import subprocess
import threading
import pathlib
import time

import files
import esi

'''ui components'''
root = tk.Tk() # main window
serenity_btn = Button(root, text='国服') # serenity button
tranquility_btn = Button(root, text='欧服') # tranquility button
path_box = ttk.Combobox(root) # path box
open_btn = Button() # open-selected-dir button
read_btn_text = tk.StringVar()
read_btn_text.set('获取角色名')
read_btn = Button(root) # refresh-files button
character_box = ttk.Treeview(root) # characters box
account_box = ttk.Treeview(root) # accounts box
overwrite_btn = Button() # overwrite button
help_btn = Button() # help button

'''variables'''
title = 'ESAM' # title
icon = '..' + os.sep + 'images' + os.sep + 'icon.ico' # icon
size = '700x600+400+400' # size
selected_btn_color = "#ABEBC6"

path_list = []  # setting directories list
selected_path = tk.StringVar() # selected path
fileReader = files.SettingFilesReader('Serenity') # to fetch names from esi
characters = [] # characters list ((id, name, last_mod_time))
accounts = [] # accounts ((id, last_mod_time))
esi_signal = True # fetch signal

'''render GUI'''
def createGUI():
    root.title(title)
    if isfile(icon):
        root.iconbitmap(icon)
    root.geometry(size)
    root.resizable(0, 0)

    # change server buttons
    top_btn_top = 0.01
    top_btn_height = 0.08
    top_btn_1_start = 0.25
    top_btn_2_start = 0.6
    top_btn_width = 0.15
    top_btn_font = ('bold', 25)
    serenity_btn["font"] = top_btn_font
    serenity_btn["command"] = lambda: change_server('Serenity')
    serenity_btn.place(relx=top_btn_1_start, rely=top_btn_top, relwidth=top_btn_width, relheight=top_btn_height)
    tranquility_btn["font"] = top_btn_font
    tranquility_btn["command"] = lambda: change_server('Tranquility')
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

    # change path button
    path_btn_start = 0.13
    path_btn_top = 0.17
    path_btn_width = 0.2
    path_btn_height = 0.07
    path_btn_font = ('bold', 16)
    change_path_btn = Button(root, text='手动设置路径', font=path_btn_font, command=change_path)
    change_path_btn.place(relx=path_btn_start, rely=path_btn_top, relwidth=path_btn_width, relheight=path_btn_height)

    # open directory button
    open_btn_start = 0.4
    open_btn_top = path_btn_top
    open_btn_width = path_btn_width
    open_btn_height = path_btn_height
    open_btn = Button(root, text='打开文件夹', font=path_btn_font, command=open_dir)
    open_btn.place(relx=open_btn_start, rely=open_btn_top, relwidth=open_btn_width, relheight=open_btn_height)

    # read names button
    read_btn_start = 0.66
    read_btn_top = path_btn_top
    read_btn_width = path_btn_width
    read_btn_height = path_btn_height
    read_btn["textvariable"] = read_btn_text
    read_btn["font"] = path_btn_font
    read_btn["command"] = start_read_names
    read_btn.place(relx=read_btn_start, rely=read_btn_top, relwidth=read_btn_width, relheight = read_btn_height)

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
    character_box_width = 0.5
    character_box_height = 0.55

    character_column_width = int(700*character_box_width/3)

    global character_box
    character_box = ttk.Treeview(root, columns=('character_id', 'character_name', 'last_mod_time'), show='headings', selectmode='browse')
    character_box.heading('character_id', text='角色ID')
    character_box.column('character_id', width=character_column_width-15, minwidth=character_column_width-15, anchor=tk.CENTER, stretch=False)
    character_box.heading('character_name', text='角色名')
    character_box.column('character_name', width=character_column_width, minwidth=character_column_width, anchor=tk.CENTER, stretch=False)
    character_box.heading('last_mod_time', text='最后修改时间')
    character_box.column('last_mod_time', width=character_column_width+15, minwidth=character_column_width+15, anchor=tk.CENTER, stretch=False)
    
    character_box.place(relx=0.01, rely=character_box_top, relwidth=character_box_width, relheight=character_box_height)
    character_scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=character_box.yview)
    character_box.configure(yscroll=character_scrollbar.set)
    character_scrollbar.place(relx=0.51, rely=character_box_top, relheight=character_box_height)

    # accounts box
    account_box_width = 0.4
    account_column_width = int(700*account_box_width/2)

    account_box_label_top = char_box_label_top
    account_box_label = Label(root, text='账号', font=char_box_label_font)
    account_box_label.place(relx=0.7, rely=account_box_label_top)

    account_box_top = account_box_label_top + 0.05
    account_box_height = character_box_height
    global account_box
    account_box = ttk.Treeview(root, columns=('account_id', 'last_mod_time'), show='headings', selectmode='browse')
    account_box.heading('account_id', text='账号ID')
    account_box.column('account_id', width=account_column_width-15, minwidth=account_column_width-15, anchor=tk.CENTER, stretch=False)
    account_box.heading('last_mod_time', text='最后修改时间')
    account_box.column('last_mod_time', width=account_column_width+15, minwidth=account_column_width+15, anchor=tk.CENTER, stretch=False)
    account_box.place(relx=0.56, rely=account_box_top, relwidth=account_box_width, relheight=character_box_height)
    account_scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=account_box.yview)
    account_box.configure(yscroll=account_scrollbar.set)
    account_scrollbar.place(relx=0.96, rely=account_box_top, relheight=account_box_height)

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

'''Change server'''
def change_server(server):
    serenity_btn["bg"] = selected_btn_color if (server == 'Serenity') else "#f0f0f0"
    tranquility_btn["bg"] = selected_btn_color if (server == 'Tranquility') else "#f0f0f0"
    fileReader.server = server
    read_dirs()
    refresh_files()    

'''Open directory dialog, select path'''
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
    stop_esi()
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
    stop_esi()
    character_box.delete(*character_box.get_children())
    account_box.delete(*account_box.get_children())
    global characters, accounts
    characters = []
    accounts = []

    characters = fileReader.read_character(selected_path.get())
    accounts = fileReader.read_account(selected_path.get())

    for c in characters:
        character_box.insert('', tk.END, values=(c))
    for a in accounts:
        account_box.insert('', tk.END, values=a)
    
'''Overwrite files'''
def overwrite():
    global character_box, account_box
    selected_c = character_box.selection()
    selected_c_id = ''
    selected_c_name = ''
    selected_c_mod = ''
    selected_a = account_box.selection()
    selected_a_id = ''
    selected_a_mod = ''
    if selected_c:
        selected_c_id = character_box.item(selected_c[0], 'values')[0]
        selected_c_name = character_box.item(selected_c[0], 'values')[1]
        selected_c_mod = character_box.item(selected_c[0], 'values')[2]
    if selected_a:
        selected_a_id = account_box.item(selected_a[0], 'values')[0]
        selected_a_mod = account_box.item(selected_a[0], 'values')[1]

    msg_c = '' if not selected_c else ('角色:' + '\n    ID: ' + selected_c_id + '\n    角色名: ' + selected_c_name + '\n    最后修改时间: ' + selected_c_mod)
    msg_a = '' if not selected_a else ('账号:' + '\n    ID: ' + selected_a_id + '\n    最后修改时间: ' + selected_a_mod)
    
    if msg_c or msg_a:
        msg_c = '<未选择角色>' if not selected_c else msg_c
        msg_a = '<未选择账号>' if not selected_a else msg_a
        confirm = messagebox.askyesno(title='确认用下面的模板覆盖所有设置？',
                            message=(msg_c + '\n\n ' + msg_a))
        if confirm:
            fileReader.overwrite(selected_path.get(), characters, selected_c_id, accounts, selected_a_id)
            refresh_files()
    else:
        messagebox.showinfo('未选择模板', '请在角色账号列表中选择模板')

'''Open help window'''
def open_help():
    messagebox.showinfo('使用说明', '选择一个角色或账号作为模板,确认覆盖后，其它的角色或账号设置会和模板一致\n\
注意事项：\n\
    - 建议在操作前作好备份（打开文件夹，将所有.dat文件复制粘贴到一个新建文件夹内）\n\
    - 如果角色在游戏内加入了一个带有密码或权限限制的频道，复制设置文件不能使其它角色也获得密码或权限\
    ')

'''Read dirs'''
def read_dirs():
    path_list = fileReader.getDirs()
    path_box['values'] = path_list
    selected_path.set(path_list[0])
    path_box.set(selected_path.get())

'''Read character names'''
def read_names():
    global character_box, esi_signal
    esi_signal = True
    esiReader = esi.EsiReader(fileReader.server)

    for i in character_box.get_children():
        if not esi_signal:
            break
        values = character_box.item(i, 'values')
        c_name = esiReader.get_character_name(values[0])
        if esi_signal:
            character_box.item(i, text='', values=(values[0], c_name, values[2]))
    stop_esi()

'''Stop fetching names from esi'''
def stop_esi():
    global esi_signal, read_btn, read_btn_text
    esi_signal = False
    read_btn_text.set('获取角色名')
    read_btn["state"] = 'normal'

'''Change read names button, start reading process in thread'''
def start_read_names():
    global read_btn, read_btn_text
    read_btn["state"] = 'disabled'
    read_btn_text.set('读取中...')
    threading.Thread(target=read_names).start()

'''Start program'''
createGUI()
change_server('Serenity')
read_dirs()
refresh_files()
root.mainloop()