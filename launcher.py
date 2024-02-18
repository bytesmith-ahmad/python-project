# This package requires to be at the top level lest the import will fail!

import os
import logging
from modules.my_module import *
from presentation.FishConsoleView import *

# Configure logger in my own tastes for debugging purposes
# in the future, may create my own logging module complete with styles
setup(logging)

# clear console
os.system("cls")

# get current path
current_path = os.getcwd()
logging.info(f"Operating from: {current_path}")

# load config (not needed for this program)

# call consoleview
FishConsoleView.start() # loop
logging.info("Program closed")

# signature
sign()
print(f"\033[2mSee logs at: {current_path}\\.log\033[0m\n")