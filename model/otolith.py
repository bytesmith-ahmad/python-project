# Code by Ahmad Al-Jabbouri

class Otolith:
    """
    Represents a Data Transfer Object (DTO) for otolith data.

    Attributes:
        source (str): The source of the otolith data.
        latin_name (str): The Latin name of the fish.
        english_name (str): The English name of the fish.
        french_name (str): The French name of the fish.
        year (int): The year of the otolith data.
        month (int): The month of the otolith data.
        number_otoliths (int): The number of otoliths.

    Methods:
        __str__(): Returns a formatted string representation of the DTO.
        toArray(): Returns a list containing the DTO attributes.
    """
    def __init__(self, source, latin_name, english_name, french_name, year, month, number_otoliths):
        """
        Initializes an OtolithDTO instance with the provided attributes.

        Args:
            source (str): The source of the otolith data.
            latin_name (str): The Latin name of the fish.
            english_name (str): The English name of the fish.
            french_name (str): The French name of the fish.
            year (int): The year of the otolith data.
            month (int): The month of the otolith data.
            number_otoliths (int): The number of otoliths.
        """
        self.source = source
        self.latin_name = latin_name
        self.english_name = english_name
        self.french_name = french_name
        self.year = year
        self.month = month
        self.number_otoliths = number_otoliths

    def __str__(self) -> str:
        """
        Returns a formatted string representation of the DTO.

        Returns:
            str: A string representation of the DTO.
        """
        return f"OtolithDTO(source={self.source}, latin_name={self.latin_name}, " \
               f"english_name={self.english_name}, french_name={self.french_name}, " \
               f"year={self.year}, month={self.month}, number_otoliths={self.number_otoliths})"

    def toArray(self):
        """
        Returns a list containing the DTO attributes.

        Returns:
            list: A list containing the DTO attributes.
        """
        return list(vars(self).values())