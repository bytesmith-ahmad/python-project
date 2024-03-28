from enum import Enum
from pathlib import PureWindowsPath as Path
from configparser import ConfigParser
from os import system
from utils import my_logger
from cutie import select as nav_menu, prompt_yes_or_no as yes_or_no
from tabulate import tabulate
from persistence.datastore import DataStore
from pypika import Query, Table, Field
from business.models.otolith import Otolith

# parent folder
src = Path(__file__).parent

class operation(Enum):
    SELECT = 0
    INSERT = 1
    UPDATE = 2
    DELETE = 3

# setup
parser = ConfigParser()
parser.read(src / 'config.ini')
db_name = src / parser['Datasources']['otolith']
table = Table('NAFO_4T_otoliths')

def connect(db):
    return DataStore(db)

def commit(db:DataStore):
    db.commit()

def select(db,table: Table,columns = '*',rowid=True) -> "Report":
    return db.execute(
        table.select('rowid', *columns) # * is for unpacking
    )

def insert(db,table: Table, values: list[object]):    
    return db.execute(
        table.insert(*[o.as_values() for o in values])
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

def map_to_otolith(rows: list[dict[str]]) -> list[Otolith]:
    return [Otolith(**row) for row in rows]

def menu0(db:DataStore):
    tables = db.get_tables()
    chosen = nav_menu(
            tables + ['\033[0m'],
            caption_indices=[len(tables)],
            deselected_prefix="\033[0m   ",
            selected_prefix=" \033[92m>\033[7m\033[0m \033[7m", # 92 = green, 7 = reverse
            selected_index=0
        )
    return tables[chosen]

def menu1(db:DataStore):
    ops = list(operation)
    chosen = nav_menu(
            ops + ['\033[0m'],
            caption_indices=[len(ops)],
            deselected_prefix="\033[0m   ",
            selected_prefix=" \033[92m>\033[7m\033[0m \033[7m", # 92 = green, 7 = reverse
            selected_index=0
        )
    return ops[chosen]

def menu2(D,focus: Table,op):
    match op:
        case operation.SELECT:
            data = gather_data(op,focus)
            report = select(D,focus,data['columns'])
        case operation.INSERT:
            data = gather_data(op)
            insert(D,focus,data['values'])
        case operation.UPDATE:
            data = gather_data(op)
            update(D,focus,data['target'],data['value'],Field('rowid'),data['id'])
        case operation.DELETE:
            data = gather_data(op)
            delete(D,focus,data['id'])
    return report

def menu3(db,table):
    return yes_or_no("Commit?")

def to_table(data:list[object], headers='firstrow'):
    matrix = []
    for obj in data:
        row = []
        for val in obj.as_values():
            row += [val]
        matrix += [row]
    return tabulate(
            headers=headers,
            tabular_data=matrix,
            tablefmt='rounded_outline'
        )

def gather_data(op:operation, table: Table = None):
    data = {}
    match op:
        case operation.SELECT:
            x = table.fields() 
            chosen = nav_menu(
                table.fields() + ['\033[0m'],
                caption_indices=[len(op)],
                deselected_prefix="\033[0m   ",
                selected_prefix=" \033[92m>\033[7m\033[0m \033[7m", # 92 = green, 7 = reverse
                selected_index=0
            )
        case operation.INSERT:
            data = gather_data(op)
            insert(D,chosen_table,data['values'])
        case operation.UPDATE:
            data = gather_data(op)
            update(D,chosen_table,data['target'],data['value'],Field('rowid'),data['id'])
        case operation.DELETE:
            data = gather_data(op)
            delete(D,chosen_table,data['id'])
    return report

# TODO Begin tests

system('cls')

# D > T > C > R
D = connect(db_name)     #* success
T = D.get_tables()       #* success
C = D.get_fields(T[0])   #* success

data = [
        Otolith('sdf','sdfs','sdfsd','sdfs',3454,65,88),
        Otolith('fgh','fgh','fgh','gh',566,45,645),
        Otolith('a','b','c','d',5996,34,86)
    ]

insert(D,T[0],data) #* success
update(D,T[0],Field('number'),99999,Field('rowid'),5) #* success
delete(D,T[0],4)    #* successs
commit(D)           #* success

chosen_table = menu0(D) #* success
fields = D.get_fields(chosen_table)
report = select(D,chosen_table)
otoliths = map_to_otolith(report.rows)
print(to_table(otoliths,headers=otoliths[0].as_keys()))
op = menu1(D) #* success
#! TABLES MUST REFERENCE DB. FIELDS MUST REFERENCE TABLES.
params = menu2(D, chosen_table, op) #todo
affirmative = menu3(D,chosen_table) #todo
if affirmative:
    D.commit()
    print("Committed")
    D.execute(f"SELECT * FROM {chosen_table}")
    