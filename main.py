import configparser

from system_logger.system_logger import system_logger
from fetch_and_fix_files.fetch_and_fix_files import fetch_and_fix_files


def driver():
    config = configparser.ConfigParser()
    config.read("./config.ini")
    my_system_logger = system_logger(config = config)
    my_system_logger.create_log("[main] Launching file fixer...", my_system_logger.get_logging_module().INFO)
    fetch_and_fix_files(my_logger=my_system_logger, config=config)

if(__name__ == "__main__"):
    driver()