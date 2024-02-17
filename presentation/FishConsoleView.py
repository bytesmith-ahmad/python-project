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

    def __init__(self):  
        self.fish_service = FishService()
        logging.info("Initiated FishConsoleView")
        
    def start(self): # begin loop
        try:
            exit = False
            while not exit:
                user_input = input("\nEnter your command (type 'help' for available commands)\n\n> ")
                logging.info(f"User entered \"{user_input}\"")
                
                processed_input = self.process(user_input)
                if processed_input.get("action") is not None:
                    exit = self.execute_action(processed_input)
        except:
            logging.exception("What happened?")
        
    
    # take raw_input, refines it, then extracts action and id where id could be null
    def process(self, raw_input):
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
    def execute_action(self, action_set):
        exit = False
        try:
            action = action_set.get("action")
            match action:
                case "exit":
                    exit = True
                case "help":
                    print(self.MENU_TEXT)
                case _:
                    logging.info(f"Executing action {action.upper()}...\n")
                    self.show(self.fish_service.execute_action(action_set))
        except ValueError:
            pass
        except:
            logging.exception("ERROR IN FishConsoleView.execute_action")
        finally:
            return exit
            
    def show(self,result):
        print("use prettyTable")
            
    def __str__(self):
        return f"{self.fish_service}"