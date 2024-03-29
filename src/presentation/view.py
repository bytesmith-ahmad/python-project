from enum import Enum
import os
from logging import info, exception
from business.controller import Controller
from cutie import select as nav_menu, select_multiple
from pypika import Table

class View:
    
    class operations(Enum):
        SELECT = 0
        INSERT = 1
        UPDATE = 2
        DELETE = 3
        COMMIT = 4
    
        def __str__(self): return self.name  # Returns only the name without the prefix
    
    @staticmethod
    def start(path_to_db):
        """
        Begin the console loop for user interaction.
        """
        try:
            os.system('cls')
            Controller.establish_connection(path_to_db)
            table = View.choose()
            exit = False
            while not exit:
                # list_ = Controller.select(table)
                # View.display(list_)
                op = View.choose_operation()
                data = View.collect_data(op=op,table=table)
                otoliths = Controller.process(op=op,table=table,data=data)
                View.display(otoliths)
        except Exception as e:
            exception("What happened?")
    
    def choose():
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
        ops = list(View.operations)
        chosen = nav_menu(
                ops + ['\033[0m'],
                caption_indices=[len(ops)],
                deselected_prefix="\033[0m   ",
                selected_prefix=" \033[92m>\033[7m\033[0m \033[7m", # 92 = green, 7 = reverse
                selected_index=0
            )
        return ops[chosen]

    def collect_data(table: Table,op: operations) -> dict:
        match op:
            case View.operations.SELECT:
                """Pick columns"""
                columns = table.columns
                ints = select_multiple(
                    options=columns,
                    ticked_indices=list(range(len(columns))),
                    minimal_count=1,
                    hide_confirm=False
                )
                data = [columns[i] for i in ints]
            case View.operations.INSERT:
                """Input for each field"""
                data = []
                for field in table.columns:
                    data += [input(str(field) + ": ")]
            case View.operations.UPDATE:
                """Need a target, value, and id"""
                data['target'] = nav_menu(
                    table.columns + ['\033[0m'],
                    caption_indices=[len(table.columns)],
                    deselected_prefix="\033[0m   ",
                    selected_prefix=" \033[92m>\033[7m\033[0m \033[7m", # 92 = green, 7 = reverse
                    selected_index=0
                )
                data['value'] = input("Value: ")
                data['id'] = input("Id: ")
                return data
            case View.operations.DELETE:
                """Need only id"""
                data = input("Id: ")
        return data

    # def menu3(db,table):
    #     return yes_or_no("Commit?")
    
    def display(list_: list):
        pass #!TODO TABULATE LIST AND STORE STATE

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    
    
    
    
    
    
    
    @classmethod
    def process(cls, raw_input):
        """
        Take raw input, refine it, and extract action and id where id could be null.
        """
        action_set = {
            "action": None,
            "arg": None
        }
        try:
            refined_input = raw_input.strip().lower().split()
            action_set["action"] = refined_input[0]
            action_set["arg"] = refined_input[1]
        except IndexError:
            if action_set["action"] is None:
                error("\033[31mERROR: CANNOT BE EMPTY, SEEK HELP\033[0m")
            else:
                pass
        except:
            exception("ERROR: SEEK HELP")  # Send exception info to both file AND console
        finally:
            return action_set
    
    @classmethod
    def execute_action(cls, action_set):
        """
        Execute the action based on user input.
        """
        exit = False
        try:
            action = action_set.get("action")
            match action:
                case "exit":
                    exit = True
                case "help":
                    print(cls.MENU_TEXT)
                case "update":
                    cls.prompt_update() 
                case _:
                    info(f"Executing action {action.upper()}...\n")
                    display_info = FishService.execute_action(action_set)  # The only connection to FishService
                    cls.execute(display_info)  # Either PrettyTable or string, both printable
        except ValueError:
            pass
        except Exception as e:
            exception("ERROR IN FishConsoleView.execute_action")
        finally:
            return exit

    @classmethod
    def prompt_update(cls):
        """
        Prompt the user for input to update data.
        """
        try:
            index = input("Enter the ID to update: ")
            column = input("Enter the column to update: ")
            new_value = input("Enter the new value: ")

            action_set = {"action": "update", "arg": index, "column": column, "new_value": new_value}
            display_info = FishService.execute_action(action_set)
            cls.execute(display_info)
        except Exception as e:
            exception("ERROR IN prompt_update")

    @classmethod
    def __str__(cls):
        """
        String representation of the class.
        """
        return f"{cls}"
