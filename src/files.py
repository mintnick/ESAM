import os
from os import listdir
from pathlib import Path
import pathlib
import esi
import time
import shutil

class SettingFilesReader:
    root = os.path.join(Path.home().__str__(), 'AppData', 'Local', 'CCP', 'EVE') # default path of server folders on Windows
    server = ''

    char_prefix = 'core_char_'
    user_prefix = 'core_user_'
    dirs = [] # directories to store EVE clients settings, based on server

    def __init__(self, server):
        self.server = server

    '''Get all directories that fit naming pattern'''
    def getDirs(self):
        if self.server == 'Tranquility':
            self.dirs = [(self.root + os.sep + f + os.sep + 'settings_Default') for f in listdir(self.root) if f.endswith('eve_sharedcache_tq_tranquility')]
        elif self.server == 'Serenity':
            self.dirs = [(self.root + os.sep + f + os.sep + 'settings_Default') for f in listdir(self.root) if f.endswith('eve_sharedcache_serenity_serenity.evepc.163.com')]
        
        return self.dirs

    '''Read all account setting files, get last modified time, return a list of tuples'''
    def read_account(self, path):
        if not os.path.isdir(path): # if path is not a directory or not exsit
            return []

        users = [] # [(id, mod_time)]

        files = [f for f in listdir(path) # all account setting files
             if os.path.isfile(os.path.join(path, f)) and f.split('.')[0].split('_')[-1].isnumeric() and f.startswith(self.user_prefix)]
        
        for f in files: # get last mod time
            filename = os.fsdecode(f)
            file_id = filename.split('.')[0].split('_')[-1]
            mod_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(path + os.sep + f)))
            users.append((file_id, mod_time))
        
        users.sort(key=lambda user: user[1], reverse=True) # last mod file first
        return users

    '''Read all character setting files, get last modified time, return a list of tuples(leave the character names as unknown)'''
    def read_character(self, path):
        if not os.path.isdir(path): # if path is not a directory or not exsit
            return []

        characters = [] # [(id, name, mod_time)]

        files = [f for f in listdir(path) # all characters setting files
             if os.path.isfile(os.path.join(path, f)) and f.split('.')[0].split('_')[-1].isnumeric() and f.startswith(self.char_prefix)]

        for f in files: # get last mod time
            filename = os.fsdecode(f)
            file_id = filename.split('.')[0].split('_')[-1]
            mod_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(path + os.sep + f)))
            characters.append((file_id, "<未知>", mod_time))

        characters.sort(key=lambda user: user[2], reverse=True) # last mod file first
        return characters

    '''Overwrite setting files'''
    def overwrite(self, path, characters, c_id, accounts, a_id):
        if c_id and characters:
            filename = self.char_prefix + c_id + '.dat'
            model_path = os.path.join(path, filename)
            for c in characters:
                if c[0] == c_id:
                    continue
                c_path = os.path.join(path, (self.char_prefix + c[0] + '.dat'))
                shutil.copyfile(model_path, c_path)
        
        if a_id and accounts:
            filename = self.user_prefix + a_id + '.dat'
            model_path = os.path.join(path, filename)
            for a in accounts:
                if a[0] == a_id:
                    continue
                a_path = os.path.join(path, (self.user_prefix + a[0] + '.dat'))
                shutil.copyfile(model_path, a_path)
        