from persistence.DataStore import DataStore
import logging

class FishService():
    def __init__(self):
        self.datastore = DataStore()
        logging.info("Initiated FishService")