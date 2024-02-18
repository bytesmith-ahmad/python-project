
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
    def load_from_csv(cls):
        # returns a collection which holds arrays respective to each row of the CSV file it reads from
        set_of_array = None
        try:
            with open(cls.DATA_SOURCE, 'r') as testIOWrapper:
                set_of_array = csv.reader(testIOWrapper)
        except FileNotFoundError:
            print(f"Error: File not found at path: {cls.DATA_SOURCE}")
        except csv.Error as e:
            print(f"Error while processing CSV file: {e}")
        finally:
            return set_of_array
        
    @classmethod
    def save_to_csv(cls,entity_map):
        if entity_map is not None:
            data_for_csv = [DataMapper.map_entity_to_array(entity_map[key]) for key in entity_map]
            try:
                with open(cls.DATA_SOURCE, 'w', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerows(data_for_csv)
            except FileNotFoundError:
                print(f"Error: File not found at path: {cls.DATA_SOURCE}")
            except csv.Error as e:
                print(f"Error while writing to CSV file: {e}")
        
    
    @classmethod
    def get_entity_map(cls):
        if not cls.initialized:
            DataStore.initialize_config()
        list_of_arrays = cls.load_from_csv()
        map = {}
        i = -1
        for a in list_of_arrays:
            map[i] = DataMapper.map_array_to_entity(a)
            i += 1
        return map