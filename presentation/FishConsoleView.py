import sys
import logging
from logical.FishService import FishService

class FishConsoleView:
    
    MENU_TEXT = """
    - SELECT *option* where option = <id> or *
    - INSERT      (launches insert wizard)
    - UPDATE <id> (launches update wizard)
    - DELETE <id>
    - exit
    """

    @classmethod
    def start(cls): # begin loop
        try:
            exit = False
            while not exit:
                user_input = input("\nEnter your command (type 'help' for available commands)\n\n> ")
                logging.info(f"User entered \"{user_input}\"")
                
                processed_input = cls.process(user_input)
                if processed_input.get("action") is not None:
                    exit = cls.execute_action(processed_input)
        except:
            logging.exception("What happened?")
        
    
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
                logging.error("\033[31mERROR: CANNOT BE EMPTY, SEEK HELP\033[0m")
            else:
                pass
        except:
            logging.exception("ERROR: SEEK HELP") # Send exception info to both file AND console
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
                    logging.info(f"Executing action {action.upper()}...\n")
                    result = FishService.execute_action(action_set) # The only connection to FishService
                    print(result) # Either PrettyTable or string, both printable
        except ValueError:
            pass
        except:
            logging.exception("ERROR IN FishConsoleView.execute_action")
        finally:
            return exit
            
    @classmethod
    def __str__(cls):
        return f"{cls}"