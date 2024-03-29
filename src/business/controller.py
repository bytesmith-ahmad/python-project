from business.models.otolith import Otolith
from persistence.datastore import DataStore
from pypika import Query, Table, Field

class Controller:
    
    db: DataStore = None
    
    @classmethod
    def establish_connection(cls, path_to_db) -> None:
        cls.db = DataStore(path_to_db)
        
    @classmethod
    def get_tables(cls):
        return cls.db.get_tables()
    
    @classmethod
    def process(cls,op,table,data):
        match op.value:
            case 0:
                return cls.select(table,data)
            case 1:
                return cls.insert(table,data)
            case 2:
                pass
            case 3:
                pass
            case 4:
                pass
            case 5:
                pass
    
    @classmethod
    def select(cls,table: Table,columns = '*',rowid=True):
        report = cls.db.execute(
            table.select('rowid', *columns) # * is for unpacking
        )
        if report.has_error():
            return ["ERROR"]
        else:
            return cls.map_to_otolith(report.rows)
        
    def insert(cls, table: Table, values: list[object]):    
        return cls.db.execute(
            table.insert(*[o.as_values() for o in values])
        )

    def update(cls, table: Table,target: Field, value,
            identifying_column: Field, identifying_value):
        return cls.db.execute(
            table.update()
            .set(target, value)
            .where(identifying_column == identifying_value)
        )

    def delete(cls, table: Table, rowid: int):
        """Query.from_(table).delete().where(table.id == id)"""
        return cls.db.execute(
            Query().from_(table).delete().where(Field('rowid') == rowid)
        )
            
    @classmethod
    def map_to_otolith(cls,rows):
        return [Otolith(**row) for row in rows]
