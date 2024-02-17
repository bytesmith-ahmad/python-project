from logical.FishService import FishService
import logging

try:
    from parse import *
except ModuleNotFoundError:
    import pip    
    pip.main(['install', parse])
    from parse import *

class FishConsoleView:
    
    # attributes defiend here function as static attributes

    def __init__(self):  
        self.fish_service = FishService()
        logging.info("Initiated FishConsoleView")
        
    def start(self): # begin loop
        while True:
            user_input = input("\nEnter your command (type 'help' for available commands): ")
            logging.info(f"User entered \"{user_input}\"")
            processed_input = self.process(user_input)
            logging.info(f"Sending\n\taction as {processed_input.get("action")}\n\tid as {processed_input.get("id")}")
    
    def process(self, raw_input):
        try:
            refined_input = raw_input.strip().lower()
            result = parse("{action} {id}",refined_input)
            action = result.named.get("action") # check if allowed
            id = int(result.named.get("id"))
            return {"action":action,"id":id}
        except:
            logging.exception(f"ERROR: {refined_input} NOT ALLOWED, SEEK HELP")
            return {"action":"ERROR","id":"ERROR"}
    
    # def printMenu():
        
    
    # def cmdMenu():
        
    
    # def printTable():
        
    
    # def processInput(String):
        
    
    # def select():
        
    
    # def select(id or (special case, all (*))):
        
    
    # def insert(id):
        
    
    # def update(id):
        
    
    # def delete(id):
        
    
    def __str__(self):
        return f"{self.fish_service_instance}"