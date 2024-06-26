from enum import Enum
import os
import sys
from logging import info, exception
from business.controller import Controller
from cutie import select as nav_menu, select_multiple
from pypika import Table
from utils.src.signature import sign
from tabulate import tabulate

class View:
    """
    Class representing the user interface view for interacting with the application.
    """

    class operations(Enum):
        """
        Enum class defining different operations available in the view.
        """
        SELECT = 0
        INSERT = 1
        UPDATE = 2
        DELETE = 3
        COMMIT = 4
        RUN_SCRIPT = 5
        EXIT = 6
    
        def __str__(self):
            """
            Returns only the name without the prefix.
            """
            return self.name

    selected_op = None
    selected_table = None
    selected_columns: list = None
    
    @staticmethod
    def start(path_to_db):
        """
        Begin the console loop for user interaction.
        """
        try:
            os.system('cls')
            Controller.establish_connection(path_to_db)
            View.selected_table = View.choose()
            exit = False
            while not exit:
                View.selected_op = View.choose_operation()
                if View.selected_op == View.operations.EXIT:
                    exit = True
                elif View.selected_op == View.operations.COMMIT:
                    os.system('cls')
                    s = Controller.process(View.selected_op)
                    print(s)
                elif View.selected_op == View.operations.RUN_SCRIPT:
                    os.system('cls')
                    print("PASTE THE SQL SCRIPT HERE:")
                    print("To end recording, do Ctrl+Z on Windows, Ctrl+D on Linux")
                    print("*************************")
                    script = sys.stdin.readlines()
                    Controller.execute_script(script)
                else: # SELECT and DML here
                    data = View.collect_data(op=View.selected_op,table=View.selected_table)
                    otoliths = Controller.process(op=View.selected_op,table=View.selected_table,data=data)
                    View.display(otoliths)
        except Exception as e:
            exception("What happened?")

    def print_table(list_: list):
        """
        Print the given list in a tabular format.
        """
        View.display(list_)
    
    def choose():
        """
        Choose a table from the available tables.
        """
        tables = Controller.get_tables()
        chosen = nav_menu(
                tables + ['\033[0m'],
                caption_indices=[len(tables)],
                deselected_prefix="\033[0m   ",
                selected_prefix=" \033[92m>\033[7m\033[0m \033[7m", # 92 = green, 7 = reverse
                selected_index=0
            )
        return tables[chosen]

    def choose_operation():
        """
        Choose an operation from the available operations.
        """
        ops = list(View.operations)
        chosen = nav_menu(
                ops + ['\033[0m'],
                caption_indices=[len(ops)],
                deselected_prefix="\033[0m   ",
                selected_prefix=" \033[92m>\033[7m\033[0m \033[7m", # 92 = green, 7 = reverse
                selected_index=0
            )
        return ops[chosen]

    def collect_data(table: Table,op: operations):
        """
        Collect data based on the selected operation.
        """
        match op:
            case View.operations.SELECT:
                """Pick columns"""
                columns = table.columns
                print("USE ARROWS ^v TO SELECT COLUMNS THEN ENTER TO CONFIRM:\n")
                ints = select_multiple(
                    options=columns,
                    ticked_indices=list(range(len(columns))),
                    minimal_count=1,
                    cursor_index=len(columns),
                    hide_confirm=False
                )
                data = [columns[i] for i in ints]
                View.selected_columns = data
            case View.operations.INSERT:
                """Input for each field"""
                data = []
                for field in table.columns:
                    data += [input(str(field) + ": ")]
            case View.operations.UPDATE:
                """Need a target, value, and id"""
                data = {}
                data['id'] = input("Which row? (id): ")
                print("Which column needs update? : ")
                target_index = nav_menu(
                    table.columns + ['\033[0m'],
                    caption_indices=[len(table.columns)],
                    deselected_prefix="\033[0m   ",
                    selected_prefix=" \033[92m>\033[7m\033[0m \033[7m", # 92 = green, 7 = reverse
                    selected_index=0
                )
                data['target'] = table.columns[target_index]
                data['value'] = input("New value: ")
                return data
            case View.operations.DELETE:
                """Need only id"""
                data = input("Input ROWID to delete: ")
            case View.operations.COMMIT:
                data = None
        return data
    
    def chunks(lst, n):
        """
        Split a list into chunks of size n.
        """
        for i in range(0, len(lst), n):
            yield lst[i:i + n]
        
    def display(data: list[object]):
        """
        Display the data in a tabular format.
        """
        headers = data[0].as_keys()
        os.system('cls')
        for group in View.chunks(data, 10):
            print(View.to_table(group,headers=headers))
            sign()

    def to_table(data:list[object], headers='firstrow'):
        """
        Convert the data into a tabular format.
        """
        matrix = []
        for obj in data:
            row = []
            for val in obj.as_values():
                row += [val]
            matrix += [row]
        T = tabulate(
                headers=headers,
                tabular_data=matrix,
                tablefmt='rounded_outline'
            )
        View.selected = T
        return T

    @classmethod
    def __str__(cls):
        """
        String representation of the class.
        """
        return f"{cls}"
