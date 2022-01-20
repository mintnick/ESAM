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

    def read_id(self, path):
        if not os.path.isdir(path):
            return [], []

        char_ids = []
        user_ids = []
        
        for file in os.listdir(path):
            filename = os.fsdecode(file)
            file_id = filename.split('.')[0].split('_')[-1]
            if file_id.isnumeric():
                if filename.startswith(self.char_prefix):
                    char_ids.append(file_id)
                elif filename.startswith(self.user_prefix):
                    user_ids.append(file_id)
        
        return char_ids, user_ids


    def readCharacters(self, path):

        characters = [] # [(id, name)]
        users = [] # [(id, last_mod_time)]

        # is directory exsits
        # directory = os.path.join(path, 'settings_Default')
        if not os.path.isdir(path):
            return [], []
        
        esiReader = esi.EsiReader(self.server)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            file_id = filename.split('.')[0].split('_')[-1]
            if file_id.isnumeric():
                if filename.startswith(char_prefix):
                    name = esiReader.getCharacterName(id)
                    characters.append((id, name))
                elif filename.startswith(user_prefix):
                    mod_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(directory + os.sep + file)))
                    users.append((id, mod_time))

        return characters, users
