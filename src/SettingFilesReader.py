from os import listdir
import os.path
from pathlib import Path

class SettingFilesReader:
    # Mac
    root = '/Users/nick'
    # root = Path.home().__str__() + '\AppData\Local\CCP\EVE\\'
    dirs = []
    character = []

    def __init__(self, server):
        if server == 'Tranquility':
            # self.dirs = [(root_path + f) for f in listdir(root_path) if f.endswith('eve_sharedcache_tq_tranquility')]
            # Mac path, for dev purpose
            self.dirs = [(self.root + f) for f in listdir(self.root) if f.endswith('EVESettings')]
        elif server == 'Serenity':
            self.dirs = [(self.root + f) for f in listdir(self.root) if f.endswith('eve_sharedcache_serenity_serenity.evepc.163.com')]
        else:
            print('Invalid server name')

    def getDirs(self):
        return self.dirs

    def readCharacters(self, path):
        # Mac
        path = path + '/settings_Default/'
        # path = path + '\settings_Default\\'
        

reader = SettingFilesReader('Tranquility')
reader.readCharacters('/Users/nick/EVESettings')