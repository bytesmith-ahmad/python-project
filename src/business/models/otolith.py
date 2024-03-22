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
    """
    def __init__(self,
        id: int = None, source: str = None, latin_name: str = None, english_name: str = None,
        french_name: str = None, year: int = None, month: int = None, number: int = None,
        **kwargs):
        """
        Initializes an Otolith instance with the provided attributes.
        """
        self.id = id
        self.source = source
        self.latin_name = latin_name
        self.english_name = english_name
        self.french_name = french_name
        self.year = year
        self.month = month
        self.number = number

    def as_values(self) -> list:
        """
        Returns a list of attribute values.

        Returns:
            List: A list containing attribute values.
        """
        return [v for v in vars(self).values() if v is not None]

    def as_keys(self) -> list:
        """
        Returns a list of attribute names.

        Returns:
            List: A list containing attribute names.
        """
        return [k for k,v in vars(self).items() if v is not None]