import pathlib
import os
import configparser
import logging

try:
    # Get path to the directory containing this script
    script_dir = pathlib.Path(__file__).resolve().parent

    # Construct paths using pathlib
    target = script_dir / ".." / "config.ini"
    fallback = pathlib.Path.home() / "Desktop" / "otolith.log"

    config = configparser.ConfigParser()
    config.read(str(target))

    if not logging.getLogger().hasHandlers():
        logging.basicConfig(filename=config['Logfile'].get('filepath', fallback),
                            filemode='w',
                            level=logging.INFO,
                            format='%(asctime)s [%(filename)s:%(lineno)d] %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S'
                            )
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        logging.getLogger('').addHandler(console)

        def info(msg: str):
            logging.info(msg)

        def exception(msg: str):
            logging.exception(msg)

except Exception as e:
    raise ImportError("Error importing my_logger")
