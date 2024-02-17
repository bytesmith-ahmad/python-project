from logical.FishService import FishService

class FishConsoleView:
    
    # attributes defiend here function as static attributes

    def __init__(self):  
        self.fish_service = FishService()
        
    def start(self): # begin loop
        while True:
            user_input = input("\nEnter your command (type 'help' for available commands): ")
            processed_input = self.parse(user_input)
    
    def parse(self, user_input):
        return {"command": "cmd", "id" : 5}
    
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