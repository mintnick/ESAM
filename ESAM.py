# ESAM: Eve Serenity Account Manager
# Arthur: Nick Ning
# Created on: 2021/7/9 10:04

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from os import listdir
from os.path import isfile, join
import os.path
import time
import urllib.request
import json
import shutil
import copy
from pathlib import Path
import threading

# Values
title = 'ESAM'
icon = 'images\icon.ico'
size = '600x300+600+400'
loading = '读取中...'
file_path = Path.home().__str__()\
            + '\AppData\Local\CCP\EVE\d_eve_sharedcache_serenity_serenity.evepc.163.com\settings_Default\\'
url_prefix = 'https://esi.evepc.163.com/latest/characters/'
url_suffix = '/?datasource=serenity'
char_prefix = 'core_char_'
user_prefix = 'core_user_'

chars = []
chars_list = []
users = []
users_list = []

files = [(file_path + f) for f in listdir(file_path)
         if isfile(join(file_path, f)) and f.split('.')[0].split('_')[-1].isnumeric()]
files.sort(key=os.path.getmtime, reverse=True)  # sort by last modified date in descending order

for f in files:
    f = f.split('\\')[-1]
    if f.startswith(char_prefix):
        chars.append(f)
    elif f.startswith(user_prefix):
        users.append(f)


def readfiles():
    for f in chars:
        char_id = (f.split('.')[0]).split('_')[-1]
        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(file_path + f)))
        # Get name from ESI
        char_url = url_prefix + char_id + url_suffix
        with urllib.request.urlopen(char_url) as url:
            data = json.loads(url.read().decode())
            name = data['name']
            chars_list.append(char_id + ' - ' + name + ' - 最后修改: ' + time_str)

    for f in users:
        user_id = (f.split('.')[0]).split('_')[-1]
        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(file_path + f)))
        users_list.append(user_id + ' - 最后修改: ' + time_str)

    char_cb['values'] = chars_list
    char_cb.current(0)
    user_cb['values'] = users_list
    user_cb.current(0)


def overwrite():
    selected_char_index = char_cb.current()
    selected_char = os.path.join(file_path, chars[selected_char_index])
    selected_user_index = user_cb.current()
    selected_user = os.path.join(file_path, users[selected_user_index])

    flag = False
    if char_var.get() == 1 and chars_list:
        flag = True
        dst = copy.deepcopy(chars)
        dst.pop(selected_char_index)
        for f in dst:
            shutil.copyfile(selected_char, os.path.join(file_path, f))

    if user_var.get() == 1 and users_list:
        flag = True
        dst = copy.deepcopy(users)
        dst.pop(selected_user_index)
        for f in dst:
            shutil.copyfile(selected_user, os.path.join(file_path, f))

    if flag:
     messagebox.showinfo("完成", "设置文件已覆盖")


'''GUI'''
# Window
window = Tk()
window.title(title)
window.iconbitmap(icon)
window.geometry(size)
window.minsize(600, 300)

# Dropdown menus
char_label = Label(window, text='选择模板角色', font=10)
char_label.place(relx=0.05, rely=0.02)

char_cb = ttk.Combobox(window, state='readonly', font=8)
char_cb.set(loading)
char_cb.place(relx=0.05, rely=0.1, relwidth=0.9, height=30)

user_label = Label(window, text='选择模板账号', font=10)
user_label.place(relx=0.05, rely=0.24)

user_cb = ttk.Combobox(window, state='readonly', font=8)
user_cb.set(loading)
user_cb.place(relx=0.05, rely=0.32, relwidth=0.9, height=30)

# Separator
separator = ttk.Separator(window, orient='horizontal')
separator.place(relx=0, rely=0.45, relwidth=1, relheight=1)

# Checkboxes
char_var = IntVar()
char_checkbox = Checkbutton(window, text='覆盖所有角色设置', font=10, variable=char_var)
char_checkbox.select()
char_checkbox.place(relx=0.1, rely=0.5)

user_var = IntVar()
user_checkbox = Checkbutton(window, text='覆盖所有账号设置', font=10, variable=user_var)
user_checkbox.select()
user_checkbox.place(relx=0.1, rely=0.6)

# Alert message
alert_label = Label(window, text='- 角色较多时读取需要一些时间\n\n- 操作前建议做好备份\n\n- 覆盖时建议关闭客户端', fg='#B03A2E', font=6, justify=LEFT)
alert_label.place(relx=0.5, rely=0.48)

# Button
btn = Button(text='确认覆盖', bg='#7FB3D5', font=('bold', 15), command=overwrite)
btn.place(relx=0.2, rely=0.8, relwidth=0.6, height=40)

window.after(100, threading.Thread(target=readfiles).start())
window.mainloop()
