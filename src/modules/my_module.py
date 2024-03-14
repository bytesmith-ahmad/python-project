# my_module.py

import logging

# Configure logger in my own tastes for debugging purposes
# in the future, may create my own logging module complete with styles
def setup(logging):
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(filename='.log',
                            filemode='w',
                            level=logging.INFO,
                            format='%(asctime)s [%(filename)s:%(lineno)d] %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S'
                            )
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        logging.getLogger('').addHandler(console)
        
def sign():
    """Prints the signature for the demo.
    Enter $psstyle in powershell to see all styles"""
    print("\n"
          +"\033[1m"  # ANSI escape for bold style
          +"\033[3m"  # ANSI escape for italic style
          +"\033[4m"  # ANSI escape for underline style
          +"\033[5m"  # ANSI escape for blinking effect
          +"\033[93m" # ANSI escape for bright yellow
          +"Code/demo by Ahmad Al-Jabbouri"
          +"\033[0m"  # This ANSI escape removes all styles
          +"\n" 
    )
    
setup(logging)
print("\n\033[3mmy_module sends their regards\033[0m\n")