from typing import Self
from prettytable import PrettyTable

class DisplayInfo:
    def __init__(self,is_table:bool,row_count:int,pretty_table:PrettyTable,index:int,error=False) -> Self:
        self.error: bool = error
        self.is_table: bool = is_table
        self.row_count: int = row_count
        self.pretty_table: PrettyTable = pretty_table
        self.index: int = index
        # add more instructions for ConsoleView as needed