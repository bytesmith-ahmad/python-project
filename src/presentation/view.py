import os
from logging import info, exception

class View:
    
    @staticmethod
    def start():
        """
        Begin the console loop for user interaction.
        """
        try:
            exit = False
            while not exit:
                os.system('cls')
                user_input = input("\nEnter your command (type 'help' for available commands)\n\n> ")
                info(f"User entered \"{user_input}\"")
                
                processed_input = cls.process(user_input)
                if processed_input.get("action") is not None:
                    exit = cls.execute_action(processed_input)
        except:
            exception("What happened?")
            
    def menu0(db:DataStore):
        tables = db.get_tables()
        chosen = nav_menu(
                tables + ['\033[0m'],
                caption_indices=[len(tables)],
                deselected_prefix="\033[0m   ",
                selected_prefix=" \033[92m>\033[7m\033[0m \033[7m", # 92 = green, 7 = reverse
                selected_index=0
            )
        return tables[chosen]

    def menu1(db:DataStore):
        ops = list(operation)
        chosen = nav_menu(
                ops + ['\033[0m'],
                caption_indices=[len(ops)],
                deselected_prefix="\033[0m   ",
                selected_prefix=" \033[92m>\033[7m\033[0m \033[7m", # 92 = green, 7 = reverse
                selected_index=0
            )
        return ops[chosen]

    def menu2(D,focus: Table,op):
        match op:
            case operation.SELECT:
                data = gather_data(op,focus)
                report = select(D,focus,data['columns'])
            case operation.INSERT:
                data = gather_data(op)
                report = insert(D,focus,data['values'])
            case operation.UPDATE:
                data = gather_data(op)
                report = update(D,focus,data['target'],data['value'],Field('rowid'),data['id'])
            case operation.DELETE:
                data = gather_data(op)
                report = delete(D,focus,data['id'])
        return report

    def menu3(db,table):
        return yes_or_no("Commit?")

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
    def execute(cls, display_info: DisplayInfo):
        """
        Execute based on the display information.
        """
        if display_info.is_table:
            pt = display_info.pretty_table
            row_count = display_info.row_count
            i = 0
            while True:
                print(pt.get_string(start=i, end=i + 10))
                sign()
                if i > row_count - 10:
                    break
                else:
                    i += 10

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
