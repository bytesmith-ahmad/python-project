# Code by Ahmad Al-Jabbouri

from pathlib import Path
from logging import info
from utils.src.config import read_ini
from utils.src.signature import sign
from presentation.view import View
from business.controller import Controller

def main():
    """
    Main function to start the program.
    """
    # get current path
    src = Path(__file__).parent
    info(f"Operating from: {src}")
    
    # load configs
    _ini = read_ini(src/'config.ini')
    
    #^^^^^^^^^^^^^^^
    from blessed import Terminal
    term = Terminal()
    x,y = term.get_location()
    print(x, y)

    #^^^^^^^^^^^^^^^^^

    # call consoleview
    View.start(src/_ini['Datasources']['database']) # loop
    info("Program closed")

    # signature
    sign()

if __name__ == "__main__":
    main()