from pathlib import PureWindowsPath as Path
from configparser import ConfigParser
from os import system
from utils import my_logger
from persistence.datastore import DataStore
from pypika import Query, Table, Field
from business.models.otolith import Otolith

# parent folder
src = Path(__file__).parent

# setup
parser = ConfigParser()
parser.read(src / 'config.ini')
db_name = src / parser['Datasources']['otolith']
table = Table('NAFO_4T_otoliths')

# class Otolith:
#     def __init__(self,
#         source,latin_name,english_name,
#         french_name,year,month,number):
#         self.source = source
#         self.latin_name = latin_name
#         self.english_name = english_name
#         self.french_name = french_name
#         self.year = year
#         self.month = month
#         self.number = number
    
#     def as_list(self):
#         return list(vars(self).values())
    
#     def get_keys(self):
#         return list(vars(self).keys())

def connect(db):
    return DataStore(db)

def select_all(db,table_name):
    q = Query().from_(table_name).select('*')
    rep = db.execute(q)
    return rep

def select(db,table_name) -> DataStore.Report:
    columns = ['source','english_name','year']
    q = Query().from_(table_name).select(*columns) # * is for unpacking
    rep = db.execute(q)
    return rep

def insert(db,table_name):
    data = [
        Otolith('sdf','sdfs','sdfsd','sdfs',3454,65,88),
        Otolith('fgh','fgh','fgh','gh',566,45,645),
        Otolith('fg','jh','df','jnhb',5996,34,86)
    ]
    q = Query().into(table).insert(*[o.as_list() for o in data])
    rep = db.execute(q)
    return rep

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

def map_to_otolith(db,table):
    rep = select(db,table)
    row = rep.rows[0]
    otos = []
    for row in rep.rows:
        otos += [Otolith(**row)]
    pass
    return otos[0]

# TODO Begin tests

system('cls')

db = connect(db_name)
# select_all(db,table)
# select(db,table)
# insert(db,table)s
#todo update(ds,table)
#todo delete(ds,table)
#todo commit(ds,table)
otolith = map_to_otolith(db,table)
v = otolith.as_values()
k = otolith.as_keys()
pass
