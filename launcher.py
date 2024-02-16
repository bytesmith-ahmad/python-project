# This package requires to be at the top level lest the import will fail!

import os
from configparser import ConfigParser
from modules.my_module import *
from presentation.fish_console_view import *

# clear console
os.system("cls")
# load config
config = ConfigParser()
config.read('config.ini')
data_source = config.get('Settings','csv_path')
# call consoleview
fish_console_view = fish_console_view()
print(fish_console_view.var)
#sign
sign()