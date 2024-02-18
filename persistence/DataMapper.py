from model.Otolith import Otolith

class DataMapper:
    
    @staticmethod
    def map_array_to_entity(cls,array):
        return Otolith(array[0],array[1],array[2],array[3],array[4],array[5],array[6])
        
    @staticmethod
    def map_entity_to_array(cls,entity):
        return [
            entity.source,
            entity.latin_name,
            entity.english_name,
            entity.french_name,
            entity.year,
            entity.month,
            entity.number_otoliths
        ]