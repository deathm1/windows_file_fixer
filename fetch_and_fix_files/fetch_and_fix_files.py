import os
import sys
import configparser
import re
import pathlib
from system_logger.system_logger import system_logger

class fetch_and_fix_files():
    @classmethod
    def __init__(self, my_logger : system_logger, config : configparser.ConfigParser()) -> None:
        self.my_logger = my_logger
        self.config = config
        self.my_logger.create_log("[fetch_files] File fetcher has been launched...", self.my_logger.get_logging_module().INFO)
        self.standardize_file_name()
    @classmethod
    def name_standardizer(self, input_string):
        mods1 = re.sub("[^a-zA-Z0-9 ]"," ",input_string)
        mods1 = " ".join(mods1.split()).strip()
        pattern = re.compile("^[a-zA-Z]+$")
        if pattern.match(mods1):
            mods1 = mods1.lower()
        my_split = mods1.split()
        # find numbers 
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
            collect_string.append(single_split)
        return "_".join(collect_string)
    @classmethod
    def standardize_file_name(self):
        try:
            self.target_directory = self.config.get("FILE_FIXER_CONFIG","TARGET_DIRECTORY")
            for root, dirs, files in os.walk(self.target_directory):
                for dir in dirs:
                    self.my_logger.create_log(f"[fetch_files] Directory Processed : {dir}", self.my_logger.get_logging_module().INFO)
                    new_directory_name = self.name_standardizer(dir)
                    os.rename(os.path.join(root, dir), os.path.join(root, new_directory_name))
                    self.my_logger.create_log(
                        f"[fetch_files] Directory name changed from [{dir}] to [{new_directory_name}]", 
                        self.my_logger.get_logging_module().INFO
                        )
                for file in files:
                    self.my_logger.create_log(f"[fetch_files] File Processed : {file}", self.my_logger.get_logging_module().INFO)
                    initial_abs_path = os.path.join(root, file)
                    my_pathlib = pathlib.Path(initial_abs_path)
                    new_file_name = f"{self.name_standardizer(my_pathlib.stem)}{my_pathlib.suffix}"
                    os.rename(initial_abs_path, os.path.join(root, new_file_name))

                    self.my_logger.create_log(
                        f"[fetch_files] File name changed from [{file}] to [{new_file_name}]", 
                        self.my_logger.get_logging_module().INFO
                        )
        except Exception as e:
            self.my_logger.create_log(
                f"[fetch_files] Something went wrong while processing files. Error => {e}", 
                self.my_logger.get_logging_module().ERROR
            )
            sys.exit(0)