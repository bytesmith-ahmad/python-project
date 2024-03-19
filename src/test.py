from pathlib import Path
from configparser import ConfigParser
from os import system
from utils import my_logger
from persistence import datastore

top = f"{__file__}\\.."

config = ConfigParser()
config.read(f"{top}\\config.ini")
otolith_db = f"{top}\\{config['Datasources']['otolith']}"

def test_connect(otolith_db):
    system('cls')
    ds = datastore.DataStore()
    ds.connect(otolith_db)
    
def test_pathlib():
    p = Path('.')
    [x for x in p.iterdir() if x.is_dir()]

# test_connect(otolith_db)
test_pathlib()