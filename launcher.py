# This package requires to be at the top level lest the import will fail!

import os
import logging
from configparser import ConfigParser
from modules.my_module import *
from presentation.FishConsoleView import *

# Configure logger for debugging purposes
setup(logging)

# clear console
os.system("cls")

# get current path
current_path = os.getcwd()
logging.info(f"Operating from: {current_path}")

# load config
try:
    config = ConfigParser()
    config.read('config.ini')
    data_source = config.get('Settings','csv_path')
except FileNotFoundError:
    logging.error("config.ini NOT FOUND!")
except:
    logging.error("Something went wrong attempting to read [Settings] from config.ini")
else:
    logging.info(f"Connected to data_source: {current_path}\\{data_source}")

# call consoleview
fish_console_view = FishConsoleView()
try:
    fish_console_view.start()
except Exception as e:
    # logging.error("ERROR: " + str(e.with_traceback(e.__traceback__)))
    logging.exception("~~~ ERROR ~~~")

#sign
sign()

print(f"\n\n\n\nSee logs at: {current_path}\\.log\n")