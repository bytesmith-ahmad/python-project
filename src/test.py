from pathlib import PureWindowsPath as Path
from configparser import ConfigParser
from os import system
from utils import my_logger
from persistence.datastore import DataStore
from pypika import Query, Table, Field

# parent folder
src = Path(__file__).parent

# setup
parser = ConfigParser()
parser.read(src / 'config.ini')
db_name = src / parser['Datasources']['otolith']
table_name = 'NAFO_4T_otoliths'

class Otolith:
    def __init__(self,
        source,latin_name,english_name,
        french_name,year,month,number):
        self.source = source
        self.latin_name = latin_name
        self.english_name = english_name
        self.french_name = french_name
        self.year = year
        self.month = month
        self.number = number
    
    def as_dict(self):
        return vars(self)
    
    def as_list(self):
        return list(vars(self).values())
    
    def get_keys(self):
        return list(vars(self).keys())

def connect(db):
    return DataStore(db)

def select_all(db,table_name):
    q = Query().from_(table_name).select('*')
    rep = db.execute(q)
    return rep

def select(db,table_name):
    columns = ['source','english_name','year']
    q = Query().from_(table_name).select(*columns) # * is for unpacking
    rep = db.execute(q)
    return rep

def insert(db,table_name):
    data = [
        Otolith('sdf','sdfs','sdfsd','sdfs',3454,65,88).as_list(),
        Otolith('fgh','fgh','fgh','gh',566,45,645).as_list(),
        Otolith('fg','jh','df','jnhb',5996,34,86).as_list()
    ]
    q = Query().into(table_name).insert(data)
    rows = db.execute(q)

def update(ds):
    dic = {'source':'src', 'latin':'latin', 'english':'english', 'french':'french', 'year':9999, 'month':12, 'number':99}
    res1 = ds.execute('INSERT',dic) #empty
    res1 = ds.execute('INSERT',dic)
    dic = {'col':'number','val':0,'rowid':1}
    res2 = ds.execute('UPDATE',dic)
    dic = {'rowid':1}
    res3 = ds.execute('DELETE',dic)
    pass

def delete(d):
    pass

# TODO Begin tests

system('cls')

db = connect(db_name)
select_all(db,table_name)
select(db,table_name)
X = insert(db,table_name)
(x,y) = (
    X.get_columns(),
    X.get_values()
)
update(ds,table_name)
delete(ds,table_name)