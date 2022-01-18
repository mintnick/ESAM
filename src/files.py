import os
from os import listdir
from pathlib import Path
import esi
import time

class SettingFilesReader:
    # Mac
    # root = '/Users/nick'
    root = Path.home().__str__() \
        + os.sep + 'AppData' \
        + os.sep + 'Local' \
        + os.sep + 'CCP' \
        + os.sep + 'EVE' \
        + os.sep
    server = ''
    dirs = []
    character = []

    def __init__(self, server):
        self.server = server

    def getDirs(self):
        if self.server == 'Tranquility':
            # self.dirs = [(root_path + f) for f in listdir(root_path) if f.endswith('eve_sharedcache_tq_tranquility')]
            # Mac path, for dev purpose
            self.dirs = [(self.root + f) for f in listdir(self.root) if f.endswith('EVESettings')]
        elif self.server == 'Serenity':
            self.dirs = [(self.root + f) for f in listdir(self.root) if f.endswith('eve_sharedcache_serenity_serenity.evepc.163.com')]
        
        return self.dirs

    def readCharacters(self, path):
        char_prefix = 'core_char_'
        user_prefix = 'core_user_'

        characters = [] # [(id, name)]
        users = [] # [(id, last_mod_time)]

        # is directory exsits
        directory = os.path.join(path, 'settings_Default')
        if not os.path.isdir(directory):
            return [], []
        
        esiReader = esi.EsiReader(self.server)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            id = filename.split('.')[0].split('_')[-1]
            if id.isnumeric():
                if filename.startswith(char_prefix):
                    name = esiReader.getCharacterName(id)
                    characters.append((id, name))
                elif filename.startswith(user_prefix):
                    mod_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(directory + os.sep + file)))
                    users.append((id, mod_time))

        return characters, users
