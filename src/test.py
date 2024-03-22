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

def connect(db):
    return DataStore(db)

def commit(db:DataStore):
    db.commit()

def select(db,t,columns = '*',rowid=True) -> DataStore.Report:
    q = t.select('rowid', *columns) # * is for unpacking
    rep = db.execute(q)
    return rep

def insert(db,t):
    data = [
        Otolith('sdf','sdfs','sdfsd','sdfs',3454,65,88), #! SINGLE QUOTES BREAK PROGRAM
        Otolith('fgh','fgh','fgh','gh',566,45,645),
        Otolith('fg','jh','df','jnhb',5996,34,86)
    ]
    q = t.insert(*[o.as_values() for o in data])
    rep = db.execute(q)
    return rep

def update(db:DataStore,t,field):
    q = t.update().set('number', 55).where(field == 2)
    db.execute(q)
    pass

def delete(d):
    pass

def map_to_otolith(rows) -> list[Otolith]:
    otos = []
    for row in rows:
        otos += [Otolith(**row)]
    return otos[0]

# TODO Begin tests

system('cls')

# D > T > C > R
D = connect(db_name)     #* success
T = D.get_tables()       #* success
C = D.get_fields(T[0])   #* success

s1 = select(D,T[0]) #* success

chosen_cols = [1, 3, 6]
c = [C[i] for i in chosen_cols]
s2 = select(D,T[0],c)   #* success

map_to_otolith(s1.rows) #* success

insert(D,Table(T[0])) #! FAIL

update(D,Table(T[0]),Field('rowid')) #! TODO

delete(ds,table) #! TODO

commit(ds,table) #^ NOT TESTED

# menu0() #optional, choose table
#! TODO
menu1() #todo choose op: select, insert, update, delete
#! TODO
menu2() #todo choose columns/vals: S:(cols), I:(*otolith), U:(icol,id,col,val), D:(icol,val)
#! TODO
menu3() #todo choose commit: commit? [Y/N] 
