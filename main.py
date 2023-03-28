import configparser
import os
from system_logger.system_logger import system_logger
from fetch_and_fix_files.fetch_and_fix_files import fetch_and_fix_files
from user_interface.user_interface import user_interface

def driver():
    config = configparser.ConfigParser()
    config.read("./config.ini")
    my_system_logger = system_logger(config = config)
    my_system_logger.create_log("[main] Launching file fixer...", my_system_logger.get_logging_module().INFO)
    my = fetch_and_fix_files(my_logger=my_system_logger, config=config)
    #my.name_standardizer("asdasdasd_ASdasdas")
    user_interface(config = config, my_logger = my_system_logger)

if(__name__ == "__main__"):
    driver()