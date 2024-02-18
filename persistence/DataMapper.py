from typing import Dict
from model.Otolith import Otolith

class DataMapper:
        
    @staticmethod
    def map_to_entity(otolith_dict:Dict[str]) -> Otolith:
        return Otolith(
            source=otolith_dict["source"],
            latin_name=otolith_dict["latin_name"],
            english_name=otolith_dict["english_name"],
            french_name=otolith_dict["french_name"],
            year=otolith_dict["year"],
            month=otolith_dict["month"],
            number_otoliths=otolith_dict["number"]
        )