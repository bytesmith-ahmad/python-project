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
        """
        Initialize DisplayInfo object.

        Parameters:
        - is_table (bool): Indicates whether the data should be displayed as a table.
        - row_count (int): Number of rows in the table.
        - pretty_table (PrettyTable): PrettyTable object representing the tabular data.
        - index (int): Index of the data.
        - error (bool): Indicates if an error occurred.
        - error_msg (str): Error message.

        Returns:
        - DisplayInfo: Instance of DisplayInfo.
        """
        self.error: bool = error
        self.error_msg: str = error_msg
        self.is_table: bool = is_table
        self.row_count: int = row_count
        self.pretty_table: PrettyTable = pretty_table
        self.index: int = index
        # add more instructions for ConsoleView as needed
