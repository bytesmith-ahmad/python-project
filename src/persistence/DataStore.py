# Code by Ahmad Al-Jabbouri

import sqlite3
from utils.my_logger import info, exception#, error, debug
from pathlib import PureWindowsPath
import os
from typing import *
import pandas as pd

class DataStore():
    """
    A class representing a data store.
    """
    
    connection: sqlite3.Connection = None
    operations: dict[int:str] = None

    @classmethod
    def connect(cls,data_source: PureWindowsPath) -> None:
        """Connects to database and configures connection"""
        
        info(f"Connecting to {data_source}...")

        con = sqlite3.connect(
            database=data_source,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        con.row_factory = sqlite3.Row # .execute() will now return Rows instead of tuples. Rows work similar to dict
        row = con.execute("select sqlite_version()").fetchone()
        for value in row:
            info(f"Successfully connected to SQLite version {value}")
        cls.connection = con
        
    @classmethod
    def initialize(cls) -> dict[int:str]:
        ops = {}
        table = "NAFO_4T_otoliths"
        ops['COLUMNS'] = f"SELECT name FROM pragma_table_info('{table}');"
        ops['SELECT_ALL'] = f"SELECT * FROM {table}"
        ops['SELECT_ONE'] = f"SELECT * FROM {table} WHERE rowid = :rowid"
        ops['INSERT'] = f"INSERT INTO {table} VALUES (:source, :latin, :english, :french, :year, :month, :number)"
        ops['UPDATE'] = f"UPDATE {table} SET :col = :val WHERE rowid = :rowid"
        ops['DELETE'] = f"DELETE FROM {table} WHERE rowid = :rowid"
        cls.operations = ops
        
    @classmethod
    def execute(cls,operation: str, params: dict = None) -> sqlite3.Row:
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
        
    @staticmethod
    def get_val(rows: list[sqlite3.Row]):
        array = []
        for row in rows:
            array += [[val for val in row]]
        return array

if __name__ == "__main__":
    # TODO TEST CODE HERE
    parent = f"{__file__}\\..\\test.py"
