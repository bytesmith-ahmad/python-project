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
    return db.execute(q)

def insert(db,table: Table, data: list[object]):    
    return db.execute(
        table.insert(*[o.as_values() for o in data])
    )

def update(db:DataStore,table: Table,target: Field, value,
           identifying_column: Field, identifying_value):
    return db.execute(
        table.update()
        .set(target, value)
        .where(identifying_column == identifying_value)
    )

def delete(db:DataStore,table: Table, rowid: int):
    """Query.from_(table).delete().where(table.id == id)"""
    return db.execute(
        Query().from_(table).delete().where(Field('rowid') == rowid)
    )

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

data = [
        Otolith('sdf','sdfs','sdfsd','sdfs',3454,65,88),
        Otolith('fgh','fgh','fgh','gh',566,45,645),
        Otolith('a','b','c','d',5996,34,86)
    ]

insert(D,T[0]) #* success

update(D,T[0],Field('rowid')) #* success

delete(D,T[0],4) #* success

commit(D) #^ NOT TESTED

# menu0() #optional, choose table
#! TODO
menu1() #todo choose op: select, insert, update, delete
#! TODO
menu2() #todo choose columns/vals: S:(cols), I:(*otolith), U:(icol,id,col,val), D:(icol,val)
#! TODO
menu3() #todo choose commit: commit? [Y/N] 
