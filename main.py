import configparser
from system_logger.system_logger import system_logger
from fetch_and_fix_files.fetch_and_fix_files import fetch_and_fix_files
from user_interface.user_interface import user_interface

def driver():
    config = configparser.ConfigParser()
    config.read("./config.ini")
    my_system_logger = system_logger(config = config)
    my_system_logger.create_log("[main] Launching file fixer...", my_system_logger.get_logging_module().INFO)
    # my = fetch_and_fix_files(my_logger=my_system_logger, config=config)
    if(int(config.get("SYSTEM","UI_TOGGLE")) == 1):
        user_interface(config = config, my_logger = my_system_logger)
    elif(int(config.get("SYSTEM","UI_TOGGLE")) == 0):
        fetch_and_fix_files(my_logger=my_system_logger,
                            config=config,
                            target_directory=config.get("FILE_FIXER_CONFIG","TARGET_DIRECTORY"),
                            save_location=config.get("FILE_FIXER_CONFIG","SAVE_LOCATION"), 
                            save_location_name=config.get("FILE_FIXER_CONFIG","SAVE_LOCATION_NAME"),
                            function_string=[int(str(func).strip()) for func in config.get("FILE_FIXER_CONFIG","FUNCTIONS").split(",")])
if(__name__ == "__main__"):
    driver()