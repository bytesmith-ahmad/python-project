from persistence.DataStore import DataStore
import logging

class FishService:
    
    INVALID_COMMAND = None #or replace by a special result#
    
    def __init__(self):
        self.datastore = DataStore()

    # action_set received from Console view and returns a PrettyTable
    def execute_action(self, action_set):
        try:
            action = action_set.get("action").upper()
            arg = action_set.get("arg")
            match action:
                case "SELECT" | "GET":
                    return self.select(arg)
                case "INSERT" | "ADD":
                    return self.insert()
                case "UPDATE" | "MOD":
                    return self.update(arg)
                case "DELETE" | "DEL":
                    return self.delete(arg)
                case _:
                    logging.error("\033[31mNO SUCH COMMAND, RETURN\033[0m")
                    return self.INVALID_COMMAND
        except:
            logging.exception("ERROR IN FishService.execute_action")

    def select(self, arg):
        try:
            if arg is not None:
                data = self.datastore.get_data_by_id(arg)
                if data:
                    print(f"Selected data: {data}")
                else:
                    print("Data not found.")
            else:
                all_data = self.datastore.get_all_data()
                print(f"Selected all data: {all_data}")
        except:
            logging.exception("ERROR IN select")

    def insert(self):
        try:
            # Placeholder logic for inserting data into the datastore
            new_data = {"id": 1, "name": "New Fish", "type": "Tropical"}
            success = self.datastore.insert_data(new_data)
            if success:
                print(f"Data inserted successfully: {new_data}")
            else:
                print("Failed to insert data.")
        except:
            logging.exception("ERROR IN insert")

    def update(self, arg):
        try:
            if arg is not None:
                # Placeholder logic for updating data in the datastore
                updated_data = {"id": arg, "name": "Updated Fish", "type": "Saltwater"}
                success = self.datastore.update_data(updated_data)
                if success:
                    print(f"Data updated successfully: {updated_data}")
                else:
                    print(f"Failed to update data with ID {arg}.")
            else:
                print("Please provide an ID for updating.")
        except:
            logging.exception("ERROR IN update")

    def delete(self, arg):
        try:
            if arg is not None:
                success = self.datastore.delete_data_by_id(arg)
                if success:
                    print(f"Deleted data with ID {arg}")
                else:
                    print(f"Data with ID {arg} not found.")
            else:
                print("Please provide an ID for deletion.")
        except:
            logging.exception("ERROR IN delete")
