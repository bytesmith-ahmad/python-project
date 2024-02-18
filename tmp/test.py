import os
import csv
from prettytable import PrettyTable

### Initialization

DATA_SOURCE = "S:\\CODE\\PYTHON_2\\tmp\\NAFO-4T-Yellowtail-Flounder-otoliths.csv"
super_list = []

# text_io = open(DATA_SOURCE)  # open file
# iterable = csv.reader(text_io)   # read file

#################################################todo

with open(DATA_SOURCE, 'r') as text_io:
    iterable = csv.reader(text_io)
    for list in iterable:
        super_list += [list]
    print(super_list[0])
################################todo

# for fish in iterable:
#     array += [fish]

# prettyTable = PrettyTable()
# prettyTable.add_rows(array)
    
# os.system('cls')
# print(prettyTable)