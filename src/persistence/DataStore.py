# Code by Ahmad Al-Jabbouri

import sqlite3
from pypika import Query
from utils.my_logger import info, exception
from pathlib import PureWindowsPath as Path

class DataStore():
    """
    A class representing a data store. Use pyPika to build and pass Query to execute!
    """

    persistence = Path(__file__).parent
    
    class Report: # wrapper for sqlite list of rows
        """Wrapper for sqlite3 Rows"""
        def __init__(self, error: sqlite3.Error = None, table: str = None, rows: list[sqlite3.Row] = None):
            self.error = error
            self.table = table
            # self.cols = None
            self.rows = rows

        def has_error(self):
            """Check if """
            return True if self.error else False

        def get_values(self) -> list[list]:
            l = []
            for row in self.rows:
                l += [[val for val in row]]
            return l

        def get_columns(self):
            return self.rows[0].keys() # get keys from first row in list

    def __init__(self, db_path: Path = None):
        self.connection: sqlite3.Connection = None
        if db_path:
            self.connect(db_path)

    def connect(self,db_path: Path) -> None:
        """Connects to database and configures connection"""
        
        info(f"Connecting to {db_path}...")
        try:
            self.connection = sqlite3.connect(
                database=db_path,
                detect_types=sqlite3.PARSE_DECLTYPES  # To use in conjuction to converters and adapters
            )
            self.connection.row_factory = sqlite3.Row # .execute() will now return Rows instead of tuples. Rows work similar to dict
            for value in self.connection.execute("SELECT sqlite_version()").fetchone():
                info(f"Successfully connected to SQLite version {value}")
        except Exception as e:
            exception(f"Failed connection: {e}")
            
    def close(self) -> None:
        self.connection.close()
        
    def commit(self) -> None:
        self.connection.commit()
    
    def execute(self,sql: Query) -> Report:
        try:
            e = None
            t = self.get_table_name(sql)
            t = sql._from[0]._table_name
            r = self.connection.execute(str(sql)).fetchall()
            if len(r) == 0:
                r = self.connection.execute(f"SELECT * FROM {t}").fetchall()
        except sqlite3.Error as sql_e:
            e = sql_e
        except Exception as ex:
            e = ex
        finally:
            return self.Report(
                error=e,
                table=t,
                rows=r
            )

    @staticmethod
    def get_table_name(sql:Query):
        t = sql._from[0]._table_name
        if t is None:
            pass

    @staticmethod
    def toCSV(data,fname="output.csv"):
        
        with open(fname,'a') as file:
            file.write(",".join([str(j) for i in data for j in i]))

    @staticmethod
    def summary(rows):
            
        # split the rows into columns
        cols = [ [r[c] for r in rows] for c in range(len(rows[0])) ]
        
        # the time in terms of fractions of hours of how long ago
        # the sample was assumes the sampling period is 10 minutes
        t = lambda col: "{:.1f}".format((len(rows) - col) / 6.0)

        # return a tuple, consisting of tuples of the maximum,
        # the minimum and the average for each column and their
        # respective time (how long ago, in fractions of hours)
        # average has no time, of course
        ret = []

        for c in cols:
            hi = max(c)
            hi_t = t(c.index(hi))

            lo = min(c)
            lo_t = t(c.index(lo))

            avg = sum(c)/len(rows)

            ret.append(((hi,hi_t),(lo,lo_t),avg))

        return ret

#TODO ############################################
    def old_execute(cls,operation: str, params: dict = None) -> sqlite3.Row:
        """Provide a valid SQL query with paramaters OR one of the following with appropriate params:\n
COLUMNS: --\nSELECT_ALL: --\nSELECT_ONE: rowid\nINSERT: source, latin, english, french, year, month, number\n
UPDATE: rowid, column, value\nDELETE: rowid\nCOMMIT: --\n
        """
        if cls.operations is None:
            cls.initialize()
        if operation.upper() in ['COLUMNS', 'SELECT_ALL','SELECT_ONE','INSERT','UPDATE','DELETE']:
            op = cls.operations[operation.upper()]
            if params is None:
                return cls.connection.execute(op).fetchall()
            else:
                return cls.connection.execute(op,params).fetchall()
        elif operation.upper() == 'COMMIT':
            cls.connection.commit()
        elif operation.upper() == 'CLOSE':
            cls.connection.close()
        else:
            return cls.connection.execute(operation,params).fetchall()

    @classmethod
    def initialize(cls,table) -> dict[int:str]:
        ops = {}
        ops['COLUMNS'] = f"SELECT name FROM pragma_table_info('{table}');"
        ops['SELECT_ALL'] = f"SELECT * FROM {table}"
        ops['SELECT_ONE'] = f"SELECT * FROM {table} WHERE rowid = :rowid"
        ops['INSERT'] = f"INSERT INTO {table} VALUES (:source, :latin, :english, :french, :year, :month, :number)"
        ops['UPDATE'] = f"UPDATE {table} SET :col = :val WHERE rowid = :rowid"
        ops['DELETE'] = f"DELETE FROM {table} WHERE rowid = :rowid"
        cls.operations = ops
        
    @staticmethod
    def get_val(rows: list[sqlite3.Row]):
        array = []
        for row in rows:
            array += [[val for val in row]]
        return array

if __name__ == "__main__":
    # TODO TEST CODE HERE
    parent = f"{__file__}\\..\\test.py"
