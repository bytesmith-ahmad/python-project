
import configparser
import csv
import logging
import os

from persistence.DataMapper import DataMapper

class DataStore():
    
    CURRENT_PATH = os.getcwd()
    DATA_SOURCE = None
    DATA_DESC = None
    initialized = False
            
    @classmethod
    def initialize_config(cls):
        try:
            config = configparser.ConfigParser()
            config.read('config.ini')
            cls.DATA_SOURCE = config.get('database', 'csv_path')
            cls.DATA_DESC = config.get('database', 'data_dict')
            cls.initialized = True
        except FileNotFoundError:
            logging.error("\033[31mconfig.ini NOT FOUND! Place one next to launcher.py\033[0m")
        except:
            logging.exception("\033[31mERROR: Something went wrong attempting to read [database] from config.ini\033[0m")
        else:
            logging.info(f"Connected to data_source: {cls.CURRENT_PATH}\\{cls.DATA_SOURCE}")
    
    @classmethod
    def get_entity_map(cls):
        try:
            if not cls.initialized:
                DataStore.initialize_config()
            super_list = cls.load_from_csv()
            map = {}
            i = 0
            for list in super_list:
                map[i] = DataMapper.map_list_to_entity(list)
                i += 1
            return map
        except Exception as e:
            logging.exception("ERROR: " + str(e))
    
    @classmethod
    def load_from_csv(cls):
        # converts an iterable obtained from csv.reader
        # to returns a superlist (a list of lists)
        super_list = []
        try:
            with open(cls.DATA_SOURCE, 'r') as csv_file:
                iterable = csv.reader(csv_file)
                for list in iterable:
                    super_list += [list]
        except FileNotFoundError:
            print(f"Error: File not found at path: {cls.DATA_SOURCE}")
        except csv.Error as e:
            print(f"Error while processing CSV file: {e}")
        finally:
            return super_list
        
    @classmethod
    def save_to_csv(cls,entity_map):
        if entity_map is not None:
            try:
                with open(cls.DATA_SOURCE, 'w', newline='') as csv_file:
                    super_list = []
                    for i in range(len(entity_map)):
                        super_list += [DataMapper.map_entity_to_list(entity_map[i])]
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerows(super_list)
            except FileNotFoundError:
                print(f"Error: File not found at path: {cls.DATA_SOURCE}")
            except csv.Error as e:
                print(f"Error while writing to CSV file: {e}")