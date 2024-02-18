from logging import info, exception, error
from prettytable import PrettyTable
from logical.FishService import FishService
from my_module import sign
from presentation.DisplayInfo import DisplayInfo

class FishConsoleView:
    
    MENU_TEXT = """
    - SELECT <id> | * (displays table)
    - INSERT          (launches insert wizard)
    - UPDATE <id>     (launches update wizard)
    - DELETE <id>
    - exit            (terminates program)
    """

    @classmethod
    def start(cls): # begin loop
        try:
            exit = False
            while not exit:
                user_input = input("\nEnter your command (type 'help' for available commands)\n\n> ")
                info(f"User entered \"{user_input}\"")
                
                processed_input = cls.process(user_input)
                if processed_input.get("action") is not None:
                    exit = cls.execute_action(processed_input)
        except:
            exception("What happened?")
        
    
    # take raw_input, refines it, then extracts action and id where id could be null
    @classmethod
    def process(cls, raw_input):
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
            exception("ERROR: SEEK HELP") # Send exception info to both file AND console
        finally:
            return action_set
    
    # returns True if exit has been signalled
    @classmethod
    def execute_action(cls, action_set):
        exit = False
        try:
            action = action_set.get("action")
            match action:
                case "exit":
                    exit = True
                case "help":
                    print(cls.MENU_TEXT)
                case _:
                    info(f"Executing action {action.upper()}...\n")
                    display_info = FishService.execute_action(action_set) # The only connection to FishService
                    cls.execute(display_info) # Either PrettyTable or string, both printable
        except ValueError:
            pass
        except:
            exception("ERROR IN FishConsoleView.execute_action")
        finally:
            return exit
        
    @classmethod
    def execute(display_info:DisplayInfo):
        if display_info.is_table:
            pt = display_info.pretty_table
            row_count = display_info.row_count
            i = 0
            while True:
                print(pt.get_string(start=i,end=i+10))
                sign()
                if i > row_count - 10:
                    break
                else:
                    i += 10
            
    @classmethod
    def __str__(cls):
        return f"{cls}"