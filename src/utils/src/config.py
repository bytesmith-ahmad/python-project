import configparser

def read_ini(file_path: str) -> dict[str, dict[str, str]]:
    """
    Reads an .ini file and loads its values.

    Args:
    - file_path (str): The path to the .ini file.

    Returns:
    - Dict[str, Dict[str, str]]: A dictionary containing the loaded values.
    """
    config = configparser.ConfigParser()
    config.read(file_path)
    
    # Initialize an empty dictionary to store the loaded values
    loaded_values: dict[str, dict[str, str]] = {}
    
    # Iterate over each section in the .ini file
    for section in config.sections():
        # Get all options (keys) and values for the current section
        options = config.options(section)
        values = {option: config.get(section, option) for option in options}
        
        # Add the values to the dictionary with the section name as the key
        loaded_values[section] = values
    
    return loaded_values

# # Example usage:
# file_path = 'example.ini'  # Replace 'example.ini' with the path to your .ini file
# loaded_values = load_ini_file(file_path)
# print(loaded_values)
