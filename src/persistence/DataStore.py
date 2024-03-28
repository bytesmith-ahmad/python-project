# Code by Ahmad Al-Jabbouri

import sqlite3
from pypika import Query, Table, Field
from utils.my_logger import info, exception
from pathlib import PureWindowsPath as Path

class DataStore():
    """
    A class representing a data store. Use pyPika to build and pass Query to execute!
    """

    persistence = Path(__file__).parent

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
        
    def get_tables(self) -> list[str]:
        rows = self.connection.execute(
            """SELECT name FROM sqlite_master WHERE
            type = 'table' AND name NOT LIKE 'sqlite%';"""
        ).fetchall()
        return [Table(v) for row in rows for v in row]
    
    def get_fields(self,T:Table) -> list[str]:
        rows = self.connection.execute(
            f"SELECT name FROM pragma_table_info({str(T)})"
        ).fetchall()
        return [Field(v,table=T) for row in rows for v in row]#[T.field(v) for row in rows for v in row]

    def execute(self,sql: Query, rowid = True) -> "Report":
        try:
            con = self.connection
            rep = self.Report(sql=sql)
            sql = str(sql).replace("*","rowid AS id, *") if rowid else str(sql)
            rows = con.execute(sql).fetchall()
            if rows == []:
                table = self.get_table_name(rep.sql)
                rows = con.execute(f"SELECT rowid AS id, * FROM {table}").fetchall()
            rep.rows = self.reveal(rows)
        except sqlite3.Error as sql_e:
            rep.error = sql_e
        except Exception as ex:
            rep.error = ex
        finally:
            return rep

    def reveal(self,rows) -> list[dict[str]]:
        revealed_rows = []
        column_names = [column for column in rows[0].keys()]
        for row in rows:
            revealed_row = {}
            for c in column_names:
                revealed_row[c] = row[c]
            revealed_rows.append(revealed_row)
        return revealed_rows

    @staticmethod
    def get_table_name(sql:Query) -> str:
        """Extracts table name from query, doesn't not work for all queries"""
        if bool(sql._from):
            """SELECT or DELETE""" # for future use
            t = sql._from[0].get_table_name()
        elif bool(sql._insert_table):
            """INSERT"""
            t = sql._insert_table.get_table_name()
        elif bool(sql._update_table):
            """UPDATE"""
            t = sql._update_table.get_table_name()
        else:
            """unknown"""
            t = "\033[31mNOT FOUND\033[0m"
        return t

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
    
    class Report: # wrapper for sqlite list of rows
        """Wrapper for sqlite3 Rows"""
        def __init__(self, error: sqlite3.Error = None, sql: Query = None, rows: list[sqlite3.Row] = None):
            self.error = error
            self.sql = sql
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

if __name__ == "__main__":
    # TODO TEST CODE HERE
    parent = f"{__file__}\\..\\test.py"
