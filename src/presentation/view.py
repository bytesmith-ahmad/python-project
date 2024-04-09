import os, sys
from blessed import Terminal
from enum import Enum
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
        FILTER = 7 # replacing SELECT
        SORT = 8
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
    fields: list = []
    unmasked_fields = []
    cache: str = ''
    display_settings: dict = {}
    
    @classmethod
    def start(c, path_to_db):
        """
        Begin the console loop for user interaction.
        """
        try:
            exit_0 = False
            while not exit_0:
                Controller.establish_connection(path_to_db)
                c.selected_table = c.choose()
                if c.selected_table == 'EXIT':
                    exit_0 = True
                    exit_1 = True
                else:
                    exit_0 = False
                    exit_1 = False
                    c.cache = c.get_table_data(c.selected_table,View.operations.SELECT)
                while not exit_1:
                    View.display(c.cache,{}) 
                    c.selected_op = c.choose_operation()
                    if c.selected_op == c.operations.EXIT:
                        exit_1 = True
                    elif c.selected_op == c.operations.COMMIT:
                        s = Controller.process(c.selected_op)
                        os.system('cls')
                        print(c.cache)
                        print(s)
                    elif c.selected_op == c.operations.RUN_SCRIPT:
                        os.system('cls')
                        print("PASTE THE SQL SCRIPT HERE:")
                        print("To end recording, do Ctrl+Z on Windows, Ctrl+D on Linux")
                        print("*************************")
                        script = sys.stdin.readlines()
                        Controller.execute_script(script)
                    elif c.selected_op == c.operations.SORT:
                        """End goal is to append order by's to SQL queries"""
                        # selected from all columns, then choose ascendign or descending
                        ordering_terms = []
                        fields = c.selected_table.columns
                        os.system('cls')
                        print(c.cache)
                        print("SORT BY (selection order preserved):")
                        indeces = select_multiple(
                            options=fields,
                            minimal_count=1,
                            cursor_index=0,
                            hide_confirm=False
                        )
                        for index in indeces:
                            i = nav_menu(
                                options= [fields[index], 'asc ^', 'desc v\033[0m'],
                                caption_indices=[0],
                                deselected_prefix="\033[0m   ",
                                selected_prefix=" \033[92m>\033[7m\033[0m \033[7m", # 92 = green, 7 = reverse
                                selected_index=1
                            )
                            direction = 'ASC' if i == 1 else 'DESC'
                            ordering_terms += [(fields[index].name,direction)]

                        unmasked = c.unmasked_fields
                        columns = unmasked if unmasked else '*'
                        rows = Controller.select(c.selected_table,columns,ordering_terms)
                        View.display(rows,{})
                    else: # SELECT and DML here
                        data = c.collect_data(op=c.selected_op,table=c.selected_table)
                        otoliths = Controller.process(op=c.selected_op,table=c.selected_table,data=data)
                        c.display(otoliths,c.display_settings)
        except Exception as e:
            exception("What happened?")

    @classmethod
    def get_table_data(c,table,op):
        """"""
        data = c.collect_data(op=op,table=table)
        return Controller.process(op=op,table=c.selected_table,data=data)
    
    def print_table(list_: list):
        """
        Print the given list in a tabular format.
        """
        View.display(list_)
    
    def choose():
        """
        Choose a table from the available tables.
        """
        options =  Controller.get_tables() + ['EXIT']
        os.system('cls')
        chosen = nav_menu(
                options + ['\033[0m'],
                caption_indices=[len(options)],
                deselected_prefix="\033[0m   ",
                selected_prefix=" \033[92m>\033[7m\033[0m \033[7m", # 92 = green, 7 = reverse
                selected_index=0
            )
        return options[chosen]

    def choose_operation():
        """
        Choose an operation from the available operations.
        """
        ops = list(View.operations)
        x,y = View.get_coordinates()
        chosen = nav_menu(
                ops + ['\033[0m'],
                caption_indices=[len(ops)],
                deselected_prefix="\033[0m   ",
                selected_prefix=" \033[92m>\033[7m\033[0m \033[7m", # 92 = green, 7 = reverse
                selected_index=0
            )
        x,y = View.get_coordinates()
        return ops[chosen]

    def collect_data(table: Table,op: operations):
        """
        Collect user input to send to controller based on the selected operation.
        """
        match op:
            case View.operations.FILTER:
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
            case View.operations.SELECT:
                """Pick columns"""
                data = table.columns
        return data
    
    def chunks(lst, n):
        """
        Split a list into chunks of size n.
        """
        for i in range(0, len(lst), n):
            yield lst[i:i + n]
        
    def display(data: list[object], settings): #TODO
        """
        Display the data in a tabular format.
        """
        if isinstance(data,str):
            # print(data)
            pass
        else:
            headers = data[0].as_keys()
            os.system('cls')
            View.cache = '' # for quick reprint
            for group in View.chunks(data, 10):
                View.cache += View.to_table(group,headers=headers)
                View.cache += sign()
            print(View.cache)

    def to_table(data:list[object], headers='firstrow') -> str:
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
    
    def get_coordinates():
        return Terminal().get_location()

    @classmethod
    def __str__(cls):
        """
        String representation of the class.
        """
        return f"{cls}"
