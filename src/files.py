import os
from os import listdir
from pathlib import Path
import pathlib
import esi
import time

class SettingFilesReader:
    # Mac
    # root = '/Users/nick'
    root = os.path.join(Path.home().__str__(), 'AppData', 'Local', 'CCP', 'EVE')
        # + os.sep + 'AppData' \
        # + os.sep + 'Local' \
        # + os.sep + 'CCP' \
        # + os.sep + 'EVE' \
        # + os.sep
    server = ''

    char_prefix = 'core_char_'
    user_prefix = 'core_user_'
    dirs = []
    character = []

    def __init__(self, server):
        self.server = server

    def getDirs(self):
        if self.server == 'Tranquility':
            self.dirs = [(self.root + os.sep + f + os.sep + 'settings_Default') for f in listdir(self.root) if f.endswith('eve_sharedcache_tq_tranquility')]
        elif self.server == 'Serenity':
            self.dirs = [(self.root + os.sep + f + os.sep + 'settings_Default') for f in listdir(self.root) if f.endswith('eve_sharedcache_serenity_serenity.evepc.163.com')]
        
        return self.dirs

    def read_account(self, path):
        if not os.path.isdir(path):
            return []

        users = [] # [(id, mod_time)]

        files = [f for f in listdir(path)
             if os.path.isfile(os.path.join(path, f)) and f.split('.')[0].split('_')[-1].isnumeric() and f.startswith(self.user_prefix)]
        
        for f in files:
            filename = os.fsdecode(f)
            file_id = filename.split('.')[0].split('_')[-1]
            mod_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(path + os.sep + f)))
            users.append((file_id, mod_time))
        
        users.sort(key=lambda user: user[1], reverse=True)
        return users


    def read_character(self, path):
        # is directory exsits
        if not os.path.isdir(path):
            return []

        characters = [] # [(id, name, mod_time)]

        files = [f for f in listdir(path)
             if os.path.isfile(os.path.join(path, f)) and f.split('.')[0].split('_')[-1].isnumeric() and f.startswith(self.char_prefix)]

        esiReader = esi.EsiReader(self.server)
        for f in files:
            filename = os.fsdecode(f)
            file_id = filename.split('.')[0].split('_')[-1]
            mod_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(path + os.sep + f)))
            characters.append((file_id, "...", mod_time))

        characters.sort(key=lambda user: user[2], reverse=True)
        for c in characters:
            c = (c[0], c[1])
        return characters
