import urllib.request
import json

class EsiReader:
    prefix = ''
    suffix = ''
    err_msg = '未读取到角色名'

    def __init__(self, server):
        if server == 'Tranquility':
            self.prefix = 'https://esi.evetech.net/latest/characters/'
            self.suffix = '/?datasource=tranquility'
        elif server == 'Serenity':
            self.prefix = 'https://esi.evepc.163.com/latest/characters/'
            self.suffix = '/?datasource=serenity'
        else:
            print('Invalid server name')

    '''Get character name by id'''
    def getCharacterName(self, id):
        url = self.prefix + id + self.suffix

        try:
            data = urllib.request.urlopen(url)
            name = json.loads(data.read().decode())['name']
            return name
        except urllib.error.HTTPError as e:
            return err_msg
