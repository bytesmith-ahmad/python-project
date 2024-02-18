from typing import Union, Dict
import prettytable
from model.Otolith import Otolith
from persistence.DataStore import DataStore
import logging

class FishService:
    
    entity_map:Dict[int,Otolith] = DataStore.select_all() # a dictionary of key-values, key being integer, value being Otolith

    # action_set received from Console view and returns a PrettyTable
    @classmethod
    def execute_action(cls, action_set):
        try:
            action = action_set.get("action").upper()
            index = action_set.get("arg")
            match action:
                case "SELECT" | "GET":
                    return cls.select(index)
                case "INSERT" | "ADD":
                    return cls.insert()
                case "UPDATE" | "MOD":
                    return cls.update(index)
                case "DELETE" | "DEL":
                    return cls.delete(index)
                case _:
                    logging.error("\033[31mNO SUCH COMMAND, RETURN\033[0m")
                    return "\033[31mERROR\033[0m"
        except:
            logging.exception("ERROR IN FishService.execute_action")

    @classmethod
    def select(cls, index:Union[int,str]):
        pt = None
        try:
            if index == '*':
                pt = cls.prepare_pretty_table(cls.entity_map)
            elif isinstance(index, int):
                pt = cls.prepare_pretty_table({index:cls.entity_map[index]})
            else:
                raise ValueError
        except ValueError:
            logging.error(f"{index} IS NOT ACCEPTED AS ARGUMENT")
        except:
            logging.exception("ERROR IN select")
        finally:
            return pt

    @classmethod
    def insert(cls):
        try:
            # Placeholder logic for inserting data into the datastore
            new_data = {"id": 1, "name": "New Fish", "type": "Tropical"}
            success = cls.datastore.insert_data(new_data)
            if success:
                print(f"Data inserted successfully: {new_data}")
            else:
                print("Failed to insert data.")
        except:
            logging.exception("ERROR IN insert")

    @classmethod
    def update(cls, arg):
        try:
            if arg is not None:
                # Placeholder logic for updating data in the datastore
                updated_data = {"id": arg, "name": "Updated Fish", "type": "Saltwater"}
                success = cls.datastore.update_data(updated_data)
                if success:
                    print(f"Data updated successfully: {updated_data}")
                else:
                    print(f"Failed to update data with ID {arg}.")
            else:
                print("Please provide an ID for updating.")
        except:
            logging.exception("ERROR IN update")

    @classmethod
    def delete(cls, arg):
        try:
            if arg is not None:
                success = cls.datastore.delete_data_by_id(arg)
                if success:
                    print(f"Deleted data with ID {arg}")
                else:
                    print(f"Data with ID {arg} not found.")
            else:
                print("Please provide an ID for deletion.")
        except:
            logging.exception("ERROR IN delete")

    @classmethod
    def prepare_pretty_table(cls,data:Dict[int,Otolith]) -> prettytable.PrettyTable:
        logging.info("Preparing table...")
        
        pretty_table = prettytable.PrettyTable()   # initialize
        pretty_table.field_names = ["id"] + Otolith.get_properties()
        
        for key, otolith in data.items():
            pretty_table.add_row([key] + otolith.get_attributes())