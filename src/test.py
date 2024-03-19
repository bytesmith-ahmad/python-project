from pathlib import PureWindowsPath as Path
# from pathlib import 
from configparser import ConfigParser
from os import system
from utils import my_logger
from persistence import datastore

# paths
src = Path(__file__).parent
ini = src / 'config.ini'

parser = ConfigParser()
parser.read(ini)
otolith_db = parser['Datasources']['otolith']
otolith_db = src / otolith_db

def test_connect(otolith_db):
    system('cls')
    ds = datastore.DataStore()
    ds.connect(otolith_db)
    
def test_pathlib():
    p = Path('.')
    [x for x in p.iterdir() if x.is_dir()]

# test_connect(otolith_db)
