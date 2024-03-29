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
    def process(cls,op,table=None,data=None):
        match op.value:
            case 0:
                return cls.select(table,data)
            case 1:
                return cls.insert(table,data)
            case 2:
                return cls.update(table,data)
            case 3:
                return cls.delete(table,data)
            case 4:
                return cls.db.commit()
            
    @classmethod
    def execute_script(cls, script):
        return cls.db.execute_script("\n".join(script))
    
    @classmethod
    def select(cls,table: Table,columns = '*',rowid=True):
        report = cls.db.execute(
            table.select(*columns)
        )
        if report.has_error():
            return ["ERROR"]
        else:
            return cls.map_to_otolith(report.rows)
        
    @classmethod
    def insert(cls, table: Table, values: list[object]):
        report = cls.db.execute(
            table.insert(*values)
        )
        if report.has_error():
            return ["ERROR"]
        else:
            return cls.map_to_otolith(report.rows)

    @classmethod
    def update(cls, table, data):
        report = cls.db.execute(
            table.update()
            .set(data['target'], data['value'])
            .where(Field('rowid') == data['id'])
        )
        if report.has_error():
            return ["ERROR"]
        else:
            return cls.map_to_otolith(report.rows)

    @classmethod
    def delete(cls, table: Table, rowid: int):
        """Query.from_(table).delete().where(table.id == id)"""
        report = cls.db.execute(
            Query().from_(table).delete().where(Field('rowid') == rowid)
        )
        if report.has_error():
            return ["ERROR"]
        else:
            return cls.map_to_otolith(report.rows)
            
    @classmethod
    def map_to_otolith(cls,rows):
        return [Otolith(**row) for row in rows]
