from typing import List


class Otolith:
    """
    Represents an otolith.

    Attributes:
        source (str): The source of the otolith data.
        latin_name (str): The Latin name of the fish.
        english_name (str): The English name of the fish.
        french_name (str): The French name of the fish.
        year (int): The year of the otolith data.
        month (int): The month of the otolith data.
        number (int): The number of otoliths.

    Methods:
        __str__(): Returns a formatted string representation of the DTO.
    """
    def __init__(self, source: str, latin_name: str, english_name: str, french_name: str, year: int, month: int, number: int):
        """
        Initializes an Otolith instance with the provided attributes.
        """
        self.source = source
        self.latin_name = latin_name
        self.english_name = english_name
        self.french_name = french_name
        self.year = year
        self.month = month
        self.number = number

    def get_attributes(self) -> List:
        """
        Returns a list of attribute values.

        Returns:
            List: A list containing attribute values.
        """
        return list(vars(self).values())

    def get_fields(self) -> List:
        """
        Returns a list of attribute names.

        Returns:
            List: A list containing attribute names.
        """
        return list(vars(self).keys())

    def __str__(self) -> str:
        """
        Returns a formatted string representation of the DTO.

        Returns:
            str: A string representation of the DTO.
        """
        return f"Otolith(source={self.source}, latin_name={self.latin_name}, " \
               f"english_name={self.english_name}, french_name={self.french_name}, " \
               f"year={self.year}, month={self.month}, number={self.number})"
