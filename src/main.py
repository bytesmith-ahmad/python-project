# Code by Ahmad Al-Jabbouri

#todo This package requires to be at the top level lest all imports will fail!

from os import getcwd
from logging import info
from presentation.FishConsoleView import *

# get current path
current_path = getcwd()
info(f"Operating from: {current_path}")

# call consoleview
FishConsoleView.start() # loop
info("Program closed")

# signature
sign()
print(f"\033[2mSee logs at: {current_path}\\.log\033[0m\n")