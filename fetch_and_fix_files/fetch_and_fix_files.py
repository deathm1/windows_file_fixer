import os
import sys
import configparser
import re
import pathlib
import shutil
import uuid
from system_logger.system_logger import system_logger

class fetch_and_fix_files():

    @classmethod
    def __init__(self, my_logger : system_logger, config : configparser.ConfigParser(),
                 target_directory : str, save_location : str, save_location_name : str, 
                 function_string : str) -> None:
        self.my_logger = my_logger
        self.config = config
        self.my_logger.create_log("[fetch_files] File fetcher has been launched...", self.my_logger.get_logging_module().INFO)
        self.target_directory = target_directory
        self.save_location = save_location
        self.save_location_name = save_location_name
        self.function_sequence = function_string

        for current_function in self.function_sequence:
            if(current_function==0):
                self.standardize_files_and_directories()
            if(current_function==1):
                self.extract_files_from()

    @classmethod
    def extract_files_from(self):
        move_location = os.path.join(self.save_location, f"{self.save_location_name}_{uuid.uuid4().hex}")
        if(os.path.exists(move_location)==False):
            os.mkdir(move_location)
        for root, dirs, files in os.walk(self.target_directory):
            for file in files:
                my_final_file =  pathlib.Path(os.path.join(move_location, file)) 
                init_loc = os.path.join(root, file)
                final_loc = os.path.join(move_location, f"{my_final_file.stem}_{uuid.uuid4().hex}{my_final_file.suffix}")
                os.rename(init_loc, final_loc)
                self.my_logger.create_log(f"[fetch_files] Files moved from [{init_loc}] to [{final_loc}]", 
                                          self.my_logger.get_logging_module().DEBUG)
        my_dir_check = os.listdir(move_location)
        if(len(my_dir_check)==0):
            os.rmdir(move_location)
            self.my_logger.create_log(f"[fetch_files] Final location was empty, hence removed [{move_location}]", self.my_logger.get_logging_module().DEBUG)
        for root, dirs, files in os.walk(self.target_directory):
            for dir in dirs:
                if(os.path.join(root, dir) != move_location):
                    remove_dir = os.path.join(root, dir)
                    shutil.rmtree(remove_dir, ignore_errors=False, onerror=None)
                    self.my_logger.create_log(f"[fetch_files] Empty Directory removed [{remove_dir}]", 
                                          self.my_logger.get_logging_module().DEBUG)

    @classmethod
    def name_standardizer(self, input_string):
        print(self.config.get("FILE_FIXER_CONFIG","REGULAR_EXPRESSION"))
        mods1 = re.sub(self.config.get("FILE_FIXER_CONFIG","REGULAR_EXPRESSION")," ",input_string)
        mods1 = " ".join(mods1.split()).strip()
        my_split = mods1.split()
        collect_string = []
        for single_split in my_split:
            find_numbers = [e for e in re.split("[^0-9]", single_split) if e != '']
            if(len(find_numbers)>0):
                for number in find_numbers:
                    single_split = single_split.replace(number, f"_{number}_")
                if(single_split[len(single_split)-1] == "_"):
                    single_split = single_split[:len(single_split)-1]
                if(single_split[0] == "_"):
                    single_split = single_split[1:len(single_split)]
            try:
                single_split = str(single_split).lower()
            except Exception as e:
                self.my_logger.create_log(f"[fetch_files] Only numbers are there in this string, hence not lower cased. Error => {e}", 
                                          self.my_logger.get_logging_module().ERROR)
            
            collect_string.append(single_split)
        return "_".join(collect_string)
    
    @classmethod
    def standardize_files_and_directories(self):
        try:
            for root, dirs, files in os.walk(self.target_directory):
                for dir in dirs:
                    self.my_logger.create_log(f"[fetch_files] Directory Processed : {dir}", self.my_logger.get_logging_module().INFO)
                    new_directory_name = self.name_standardizer(dir)
                    os.rename(os.path.join(root, dir), os.path.join(root, new_directory_name))
                    self.my_logger.create_log(f"[fetch_files] Directory name changed from [{dir}] to [{new_directory_name}]", 
                        self.my_logger.get_logging_module().DEBUG)
                for file in files:
                    self.my_logger.create_log(f"[fetch_files] File Processed : {file}", self.my_logger.get_logging_module().INFO)
                    initial_abs_path = os.path.join(root, file)
                    my_pathlib = pathlib.Path(initial_abs_path)
                    new_file_name = f"{self.name_standardizer(my_pathlib.stem)}{my_pathlib.suffix}"
                    os.rename(initial_abs_path, os.path.join(root, new_file_name))
                    self.my_logger.create_log(f"[fetch_files] File name changed from [{file}] to [{new_file_name}]", 
                        self.my_logger.get_logging_module().DEBUG)
        except Exception as e:
            self.my_logger.create_log(f"[fetch_files] Something went wrong while processing files. Error => {e}", 
                self.my_logger.get_logging_module().ERROR)
            sys.exit(0)