import configparser
import os.path

def get_config(section,key=None):
    config = configparser.ConfigParser()
    dir = os.path.dirname(os.path.dirname(__file__))
    file_path = dir + '/config/common.ini'
    config.read(file_path,encoding='utf-8')
    if key!=None:
        return config.get(section, key)
    else:
        return config.items(section)

