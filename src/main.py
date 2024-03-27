# Code by Ahmad Al-Jabbouri

from pathlib import Path
from logging import info
from presentation.view import View
from utils.signature import sign

# get current path
src = Path(__file__).parent
info(f"Operating from: {src}")

# call consoleview
View.start() # loop
info("Program closed")

# signature
sign()
print(f"\033[2mSee logs at: {src/".log"}\033[0m\n")
