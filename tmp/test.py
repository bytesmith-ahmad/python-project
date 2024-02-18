import os
import csv
from prettytable import PrettyTable
from typing import Union
import pandas as pd

# Code by Ahmad Al-Jabbouri

class Otolith:
    """
    Represents a Data Transfer Object (DTO) for otolith data.

    Attributes:
        source (str): The source of the otolith data.
        latin_name (str): The Latin name of the fish.
        english_name (str): The English name of the fish.
        french_name (str): The French name of the fish.
        year (int): The year of the otolith data.
        month (int): The month of the otolith data.
        number_otoliths (int): The number of otoliths.

    Methods:
        __str__(): Returns a formatted string representation of the DTO.
        toArray(): Returns a list containing the DTO attributes.
    """
    def __init__(self, source, latin_name, english_name, french_name, year, month, number_otoliths):
        """
        Initializes an OtolithDTO instance with the provided attributes.

        Args:
            source (str): The source of the otolith data.
            latin_name (str): The Latin name of the fish.
            english_name (str): The English name of the fish.
            french_name (str): The French name of the fish.
            year (int): The year of the otolith data.
            month (int): The month of the otolith data.
            number_otoliths (int): The number of otoliths.
        """
        self.source = source
        self.latin_name = latin_name
        self.english_name = english_name
        self.french_name = french_name
        self.year = year
        self.month = month
        self.number_otoliths = number_otoliths

    def __str__(self) -> str:
        """
        Returns a formatted string representation of the DTO.

        Returns:
            str: A string representation of the DTO.
        """
        return f"OtolithDTO(source={self.source}, latin_name={self.latin_name}, " \
               f"english_name={self.english_name}, french_name={self.french_name}, " \
               f"year={self.year}, month={self.month}, number_otoliths={self.number_otoliths})"

    def toArray(self):
        """
        Returns a list containing the DTO attributes.

        Returns:
            list: A list containing the DTO attributes.
        """
        return list(vars(self).values())

DATA_SOURCE = "S:\\CODE\\PYTHON_2\\tmp\\NAFO-4T-Yellowtail-Flounder-otoliths.csv"

def test_1():
    with open(DATA_SOURCE, 'r') as text_io:
        iterable = csv.reader(text_io)
        id_column = []
        super_list = []
        for list in iterable:
            super_list += [list]

def test_2():
    from prettytable import PrettyTable
    x = PrettyTable()
    x.field_names = super_list[0]
    super_list.pop(0)
    x.add_rows(super_list)
    x.add_autoindex()
    print(x)
    x.del_column("Index")
    print(x._rows[0])
    
def test_3():
    data_frame = None
    data_frame = pd.read_csv(DATA_SOURCE)
    pd.options.display.max_rows = 100
    print(data_frame.to_string()) 
    print(pd.options.display.max_rows) 
    print("________________")
    # data_frame.loc[3,"source"] = "REPLACED"
    # data_frame.to_csv(DATA_SOURCE,index=False)
    # data_frame = pd.read_csv(DATA_SOURCE)
    # print(data_frame)

"""dataframe -> Series -> Otolith-compatible dictionary"""
def select(*args):
    if len(args) == 0:
        df = pd.read_csv(DATA_SOURCE)
        print(range(len(df.index)))
        idx = []
        lst = []
        
        for i in range(len(df.index)):
            idx.append(i)
            lst.append(select(i))
        
        for i in range(len(df.index)):
            print(i)
            print(list(lst[i].values()))
            
        pt = PrettyTable()
        pt.field_names = ["id"] + list(lst[0].keys())
        
        for i in range(len(lst)):
            pt.add_row([idx[i]] + list(lst[i].values()))
        
        # In presentation
        print(df)
        i = 0
        while True:
            print(pt.get_string(start=i,end=i+10))
            print("hello")
            if i > len(idx) - 10:
                break
            else:
                i += 10 
        
    if len(args) == 1:
        i = args[0]
        df = pd.read_csv(DATA_SOURCE)
        series = df.loc[i]
        map = {
            "source":series.loc["source"],
            "latin_name": series.loc["latin.name_nom.latin"],
            "english_name": series.loc["english.name_nom.anglais"],
            "french_name": series.loc["french.name_nom.français"],
            "year": series.loc["year_année"],
            "month": series.loc["month_mois"],
            "number": series.loc["number.otoliths_nombre.otolithes"]
        }
        return map
    
    # to get list f values: list(map.values())

def update(id: int, column: str, new_val: Union[str,int]) -> int:
    df = pd.read_csv(DATA_SOURCE)
    df.loc[id,column] = new_val
    df.to_csv(DATA_SOURCE,index=False)
    
def insert():
    pd.options.display.max_rows = 80
    df = pd.read_csv(DATA_SOURCE)
    data = [["SRC","LATIN","ENG","FR",10000,100,9999999999999]]
    new_df = pd.DataFrame(data,columns=list(df.columns))
    # df = df + new_df
    df = pd.concat([df,new_df])
    df.to_csv(DATA_SOURCE,index=False)
    print(df)

def test_entity_to_list():
    oto = Otolith("oto","oto","oto","oto",8888,888,888888)
    print(vars(oto).keys())

test_entity_to_list()

# update(12,y,9999999999)
# insert()
# select()