"""
Otolith Data Processing Script

This script reads otolith data from a CSV file, creates OtolithDTO objects, and displays the data in a PrettyTable.

Author: Ahmad Al-Jabbouri

Usage:
- Ensure the pathToFishCSV variable is set to the correct path of the CSV file.
- Execute the script to process the data and display the PrettyTable.

Dependencies:
- CSV module for .csv parsing
- DTO module with OtolithDTO class.
- PrettyTable module for table formatting.

References:
- https://dev.to/izabelakowal/some-ideas-on-how-to-implement-dtos-in-python-be3
- https://vglushko.github.io/design/2022/10/27/dto-in-python.html
- https://pypi.org/project/prettytable/
- https://www.w3schools.com/python/python_iterators.asp
- https://peps.python.org/pep-0257/
"""

import os
import csv
from DTO import *
from prettytable import PrettyTable

def sign():
    """Prints the signature for the demo."""
    print("Code/demo by Ahmad Al-Jabbouri")

### Initialization

pathToFishCSV = __file__ + '/../NAFO-4T-Yellowtail-Flounder-otoliths.csv'
row_counter = 0
row_limit = 10    # Maximum number of records to be processed
data_array = []

try:
    fishCSV = open(pathToFishCSV)  # open file
    fishes = csv.reader(fishCSV)   # read file

    for fish in fishes:
        try:
            # Create DTO for current line of CSV
            dto = OtolithDTO(fish[0], fish[1], fish[2], fish[3],
                             fish[4], fish[5], fish[6])
            # Insert into data structure as required
            data_array.append(dto)
            # Loop control
            row_counter += 1
            if row_counter == row_limit + 1:  # Excluding headers from count
                break
        except IndexError:
            print(f"Invalid row: {fish}")

    # Discard headers
    data_array.pop(0)

### Prepare table for display

    # Initiate table
    prettyTable = PrettyTable()
    # Add headers
    prettyTable.field_names = list(vars(data_array[0]))  
    # Add records
    for dto in data_array:
        prettyTable.add_row(dto.toArray())

### Output
        
    os.system('cls')
    print(prettyTable)
    print("\nOUTPUT BY: AHMAD AL-JABBOURI 041068196")
    print()

except FileNotFoundError:
    print(f"Error: File not found at path: {pathToFishCSV}")

except csv.Error as e:
    print(f"Error while processing CSV file: {e}")

finally:
    if 'fishCSV' in locals() and fishCSV is not None:
        fishCSV.close()