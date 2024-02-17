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
            x = self.process(user_input)
    
    def process(self, user_input):
        user_input.trim().lower
        parsed_input = parse("{}{}",user_input)
        print(type(parsed_input),parsed_input)
    
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