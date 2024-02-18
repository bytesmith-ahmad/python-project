from model.Otolith import Otolith

class DataMapper:
    
    @staticmethod
    def map_list_to_entity(list):
        return Otolith(list[0],list[1],list[2],list[3],list[4],list[5],list[6])
        
    @staticmethod
    def map_entity_to_list(entity):
        return [
            entity.source,
            entity.latin_name,
            entity.english_name,
            entity.french_name,
            entity.year,
            entity.month,
            entity.number_otoliths
        ]