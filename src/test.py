from pathlib import PureWindowsPath as Path
# from pathlib import 
from configparser import ConfigParser
from os import system
from utils import my_logger
from persistence.datastore import DataStore

# paths
src = Path(__file__).parent
ini = src / 'config.ini'

parser = ConfigParser()
parser.read(ini)
otolith_db = parser['Datasources']['otolith']
otolith_db = src / otolith_db

def test_connect(otolith_db):
    system('cls')
    ds = DataStore()
    ds.connect(otolith_db)
    
def test_pathlib():
    p = Path('.')
    [x for x in p.iterdir() if x.is_dir()]

def test_select(ds:DataStore):
    rows = ds.execute('columns')
    columns = [col[0] for col in ds.get_val(rows)]
    rows1 = ds.execute('SELECT_ALL')
    rows2 = ds.execute('SELECT_ONE',{'rowid':1})
    pass

def test_update(ds):
    dic = {'source':'src', 'latin':'latin', 'english':'english', 'french':'french', 'year':9999, 'month':12, 'number':99}
    res1 = ds.execute('INSERT',dic) #empty
    res1 = ds.execute('INSERT',dic)
    dic = {'col':'number','val':0,'rowid':1}
    res2 = ds.execute('UPDATE',dic)
    dic = {'rowid':1}
    res3 = ds.execute('DELETE',dic)
    pass

system('cls')
ds = DataStore()
ds.connect(otolith_db)
    
test_update(ds)
test_select(ds)