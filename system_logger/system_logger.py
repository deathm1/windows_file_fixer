import os
import sys
import time
import logging
import configparser
class system_logger():
    @classmethod
    def __init__(self, config : configparser.ConfigParser()) -> None:
        LOG_LOCATION = config.get("SYSTEM", "LOG_LOCATION")
        LOG_DIRECOTRY = config.get("SYSTEM", "LOG_DIRECOTRY")
        LOG_FILE_NAME = config.get("SYSTEM", "LOG_FILE_NAME")
        self.file_logging_enabled = False if (int(config.get("SYSTEM", "ENABLE_FILE_LOGGING"))==0) else True
        self.console_logging_enabled = False if (int(config.get("SYSTEM", "ENABLE_CONSOLE_LOGGING"))==0) else True
        select_log_dir = None
        select_log_folder = None
        if(os.path.exists(LOG_LOCATION)==False):
            select_log_dir = os.getcwd()
        else:
            select_log_dir = LOG_LOCATION
        if(LOG_DIRECOTRY == None or LOG_DIRECOTRY == ""):
            select_log_folder = "logs"
        else:
            select_log_folder = LOG_DIRECOTRY
        create_directory_location = os.path.join(select_log_dir, select_log_folder)
        my_dir_location = None
        if(os.path.exists(create_directory_location)):
            my_dir_location = create_directory_location
        else:
            os.mkdir(create_directory_location)
            my_dir_location = create_directory_location
        my_current_date = time.strftime("%d-%m-%Y", time.localtime())
        my_current_day_folder = os.path.join(my_dir_location, my_current_date)
        if(os.path.exists(my_current_day_folder) == False):
            os.mkdir(my_current_day_folder)
        self.my_file_name = os.path.join(my_current_day_folder, f"{LOG_FILE_NAME}_{time.time()}.log")

    @classmethod
    def get_logging_module(self):
        return logging
    @classmethod
    def create_log(self, my_log_message, log_level):
        log_format = '[%(asctime)s][%(levelname)s][%(filename)s][%(lineno)d]: %(message)s'
        log = logging.getLogger(__name__) 
        if(self.console_logging_enabled == True and self.file_logging_enabled==False):                                                  
            handler = logging.StreamHandler(sys.stdout)                                        
            log.addHandler(handler)
            logging.basicConfig(level=log_level, format=log_format)
        else:
            logging.basicConfig(
                filename=self.my_file_name, 
                level=logging.DEBUG, 
                format=log_format, 
                filemode="a"
            )
        if(log_level == logging.DEBUG):
            logging.debug(my_log_message)
        elif(log_level == logging.INFO):
            logging.info(my_log_message)
        elif(log_level == logging.WARNING):
            logging.warning(my_log_message)
        elif(log_level == logging.ERROR):
            logging.error(my_log_message)
        elif(log_level == logging.CRITICAL):
            logging.critical(my_log_message)