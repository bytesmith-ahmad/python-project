from typing import Union, Dict
from prettytable import PrettyTable
from model.Otolith import Otolith
from persistence.DataStore import DataStore
import logging

from presentation.DisplayInfo import DisplayInfo

class FishService:
    """
    Service class for fish-related operations.

    Attributes:
        entity_map (Dict[int, Otolith]): A dictionary of key-values, where the key is an integer and the value is an Otolith.

    Methods:
        execute_action(action_set) -> DisplayInfo: Executes a fish-related action based on the provided action set.
        select(index: Union[int, str]) -> DisplayInfo: Selects fish-related information based on the provided index.
        insert() -> DisplayInfo: Inserts new fish-related data into the datastore.
        update(index: int, column: str, new_val: Union[str, int]) -> DisplayInfo: Updates fish-related data in the datastore.
        delete(index: Union[int, str]) -> DisplayInfo: Deletes fish-related data from the datastore.
        prepare_display_info(data: Dict[int, Otolith]) -> DisplayInfo: Prepares display information for fish-related data.
    """

    entity_map: Dict[int, Otolith] = DataStore.select_all()

    @classmethod
    def execute_action(cls, action_set) -> DisplayInfo:
        """
        Executes a fish-related action based on the provided action set.

        Args:
            action_set (dict): A dictionary containing information about the action to be executed.

        Returns:
            DisplayInfo: An object containing information for display.
        """
        try:
            action = action_set.get("action").upper()
            index = action_set.get("arg")
            match action:
                case "SELECT" | "GET":
                    return cls.select(index)
                case "INSERT" | "ADD":
                    return cls.insert()
                case "UPDATE" | "MOD":
                    col = action_set["column"]
                    new = action_set["new_value"]
                    return cls.update(index, col, new)
                case "DELETE" | "DEL":
                    return cls.delete(index)
                case _:
                    logging.error("\033[31mNO SUCH COMMAND, RETURN\033[0m")
                    return DisplayInfo(error=True, error_msg="\033[31mERROR\033[0m")
        except Exception as e:
            logging.exception("ERROR IN FishService.execute_action")

    @classmethod
    def select(cls, index: Union[int, str]) -> DisplayInfo:
        """
        Selects fish-related information based on the provided index.

        Args:
            index (Union[int, str]): The index or identifier for the fish-related information.

        Returns:
            DisplayInfo: An object containing information for display.
        """
        di = DisplayInfo()
        try:
            if index == '*':
                di = cls.prepare_display_info(cls.entity_map)
            elif index.isdigit():
                index = int(index)
                di = cls.prepare_display_info({index: cls.entity_map[index]})
            else:
                raise ValueError
        except ValueError as ve:
            logging.error(f"{index} IS NOT ACCEPTED AS ARGUMENT")
            di = DisplayInfo(error=True)
        except Exception as e:
            logging.exception("ERROR IN select:" + e)
            di = DisplayInfo(error=True)
        finally:
            return di

    @classmethod
    def insert(cls) -> DisplayInfo:
        """
        Inserts new fish-related data into the datastore.

        Returns:
            DisplayInfo: An object containing information for display.
        """
        try:
            new_data = {"source": "New Source", "latin_name": "New Latin", "english_name": "New English",
                        "french_name": "New French", "year": 2024, "month": 2, "number": 42}

            DataStore.insert([list(new_data.values())])
            cls.entity_map = DataStore.select_all()

            print(f"Data inserted successfully: {new_data}")
            return cls.prepare_display_info({len(cls.entity_map) - 1: cls.entity_map[len(cls.entity_map) - 1]})
        except Exception as e:
            logging.exception("ERROR IN insert")
            return DisplayInfo(error=True, error_msg=str(e))

    @classmethod
    def update(cls, index: int, column: str, new_val: Union[str, int]) -> DisplayInfo:
        """
        Updates fish-related data in the datastore.

        Args:
            index (int): The index or identifier for the fish-related information.
            column (str): The column to be updated.
            new_val (Union[str, int]): The new value to be assigned.

        Returns:
            DisplayInfo: An object containing information for display.
        """
        try:
            if str(index).isdigit():
                index = int(index)
                DataStore.update(index, column, new_val)
                cls.entity_map = DataStore.select_all()
                return cls.prepare_display_info({index: cls.entity_map[index]})
            else:
                raise ValueError("Invalid index format")
        except ValueError as ve:
            logging.error(f"{index} IS NOT ACCEPTED AS ARGUMENT")
            return DisplayInfo(error=True)
        except Exception as e:
            logging.exception("ERROR IN update:" + str(e))
            return DisplayInfo(error=True, error_msg="Error in update")

    @classmethod
    def delete(cls, index: Union[int, str]) -> DisplayInfo:
        """
        Deletes fish-related data from the datastore.

        Args:
            index (Union[int, str]): The index or identifier for the fish-related information.

        Returns:
            DisplayInfo: An object containing information for display.
        """
        try:
            index = int(index)
            if index is not None:
                DataStore.delete(index)
                cls.entity_map = DataStore.select_all()

                print(f"Deleted data with ID {index}")
                return cls.prepare_display_info({index: cls.entity_map[index]})
            else:
                print("Please provide an ID for deletion.")
                return DisplayInfo(error=True, error_msg="Please provide an ID for deletion.")
        except Exception as e:
            logging.exception("ERROR IN delete")
            return DisplayInfo(error=True, error_msg=str(e))

    @classmethod
    def prepare_display_info(cls, data: Dict[int, Otolith]) -> DisplayInfo:
        """
        Prepares display information for fish-related data.

        Args:
            data (Dict[int, Otolith]): A dictionary containing fish-related data.

        Returns:
            DisplayInfo: An object containing information for display.
        """
        logging.info("Preparing display information...")

        pt = PrettyTable()
        pt.field_names = ["id"] + list(data.values())[0].get_fields()

        count = 0
        for key, otolith in data.items():
            pt.add_row([key] + otolith.get_attributes())
            count += 1

        return DisplayInfo(
            is_table=True,
            row_count=count,
            pretty_table=pt
        )
