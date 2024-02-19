from typing import Self
from prettytable import PrettyTable

class DisplayInfo:
    def __init__(
        self,
        is_table: bool = True,
        row_count: int = 0,
        pretty_table: PrettyTable = None,
        index: int = 0,
        error: bool = False,
        error_msg: str = "") -> Self:
        self.error: bool = error
        self.error_msg: str = error_msg
        self.is_table: bool = is_table
        self.row_count: int = row_count
        self.pretty_table: PrettyTable = pretty_table
        self.index: int = index
        # add more instructions for ConsoleView as needed