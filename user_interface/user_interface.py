import os
import threading
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import *
from configparser import ConfigParser
from system_logger.system_logger import system_logger
from fetch_and_fix_files.fetch_and_fix_files import fetch_and_fix_files
class user_interface():
    @classmethod
    def __init__(self, config : ConfigParser, my_logger : system_logger) -> None:
        self.my_logger = my_logger
        self.config = config
        self.my_logger.create_log("[user_interface] Launching User Interface...", self.my_logger.get_logging_module().INFO)
        try:
            self.root = Tk()
            self.frame = ttk.Frame(self.root, padding=10)
            w = int(self.config.get("USER_INTERFACE","WIDTH"))
            h = int(self.config.get("USER_INTERFACE","HEIGHT"))
            ws = self.root.winfo_screenwidth()
            hs = self.root.winfo_screenheight()
            x = (ws/2) - (w/2)
            y = (hs/2) - (h/2)
            self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
            # self.root.iconbitmap(os.path.join(os.getcwd(), self.config.get("USER_INTERFACE","ICON")))
            self.my_logger.create_log("[user_interface] Launching Interface elements.", self.my_logger.get_logging_module().INFO)
            self.root.title(str(self.config.get("USER_INTERFACE","WINDOW_TITLE")))
            self.ui_elements()
            self.frame.grid()
            self.root.mainloop()
        except Exception as e:
            self.my_logger.create_log(f"[user_interface] Something went wrong. Error =>{e}", self.my_logger.get_logging_module().ERROR)

    @classmethod
    def ui_elements(self):
        menu_bar=Menu(self.root)
        self.root.config(menu=menu_bar) 
        file_menu= Menu(menu_bar, tearoff=0)  
        file_menu.add_command(label="Exit", command=self._quit)   
        help_menu= Menu(menu_bar, tearoff=0)  
        help_menu.add_command(label="About", command=self.help_window) 
        self.a = Label(self.root, text = "Target Directory").grid(row = 0,column = 0, padx=5, pady=2)
        self.b = Label(self.root, text = "Regular Expression").grid(row = 1,column = 0, padx=5, pady=2)
        self.c = Label(self.root, text = "Save Location").grid(row = 2, column = 0, padx=5, pady=2)
        self.d = Label(self.root, text = "Save Location Name").grid(row = 3, column = 0, padx=5, pady=2)
        self.e = Label(self.root, text = "Function Order ( , delimited)").grid(row = 4, column = 0, padx=5, pady=2)
        self.f = Label(self.root, text = "0 - Convert file and directory names to snake case.\n1 - Take all the files to a target directory as unique files.")
        self.f.grid(row = 6, column = 0, padx=5, pady=5)
        self.a1 = Entry(self.root, width=50)
        self.a1.grid(row = 0, column = 1, padx=5, pady=2)
        self.b1 = Entry(self.root, width=50)
        self.b1.grid(row = 1, column = 1, padx=5, pady=2)
        self.c1 = Entry(self.root, width=50)
        self.c1.grid(row = 2, column = 1, padx=5, pady=2)
        self.d1 = Entry(self.root, width=50)
        self.d1.grid(row = 3, column = 1, padx=5, pady=2)
        self.e1 = Entry(self.root, width=50)
        self.e1.grid(row = 4, column = 1, padx=5, pady=2)
        self.a1.insert(0, self.config.get("FILE_FIXER_CONFIG","TARGET_DIRECTORY"))
        self.b1.insert(0, self.config.get("FILE_FIXER_CONFIG","REGULAR_EXPRESSION"))
        self.c1.insert(0, self.config.get("FILE_FIXER_CONFIG","SAVE_LOCATION"))
        self.d1.insert(0, self.config.get("FILE_FIXER_CONFIG","SAVE_LOCATION_NAME"))
        self.e1.insert(0, self.config.get("FILE_FIXER_CONFIG","FUNCTIONS"))
        self.run = Button(self.root, text="Run", command=self.traitement, width=20)
        self.run.grid(row = 7, column=1, padx=5, pady=2)
        self.progress = Progressbar(self.root, orient = HORIZONTAL,length = 100, mode = 'indeterminate')
        menu_bar.add_cascade(label="Options", menu=file_menu) 
        menu_bar.add_cascade(label="Help", menu=help_menu) 

    @classmethod
    def help_window(self):
        messagebox.showinfo(f'[v{self.config.get("SYSTEM","VERSION")}] About', f'''Hi guys, this is a simple app which helps you organize your files. The app has been tested and is working fine. IF YOU MESS UP YOUR FILES, IT IS NOT MY RESPONSIBILITY. Test this app on a prototype/test directory and then use it on your files.\nMade with love, roganjosh, sambar, idli, pani puri and butter chicken in India.''')

    @classmethod
    def check_if_string_valid(self, input_str : str):
        if(input_str!=None and input_str!=""):
            return True
        return False
    
    @classmethod
    def run_tasks(self):
        TARGET_DIRECTORY = self.a1.get()
        REGULAR_EXPRESSION = self.b1.get()
        SAVE_LOCATION = self.c1.get()
        SAVE_LOCATION_NAME = self.d1.get()
        FUNCTIONS = self.e1.get()
        if(self.check_if_string_valid(TARGET_DIRECTORY) and 
            self.check_if_string_valid(REGULAR_EXPRESSION) and 
            self.check_if_string_valid(SAVE_LOCATION) and 
            self.check_if_string_valid(SAVE_LOCATION_NAME) and 
            self.check_if_string_valid(FUNCTIONS)):
            fetch_and_fix_files(
                my_logger=self.my_logger,
                config=self.config,
                target_directory=TARGET_DIRECTORY,
                save_location=SAVE_LOCATION,
                save_location_name=SAVE_LOCATION_NAME,
                function_string=[int(str(func).strip()) for func in FUNCTIONS.split(",")]
            )
            messagebox.showinfo("Completed", "All tasks completed please check the target directory.\nHave Fun :)")
            self.my_logger.create_log(f"[user_interface] All tasks completed please check the target directory.", 
                                      self.my_logger.get_logging_module().INFO)
        else:
            messagebox.showerror("Information Mission", "Information is missing, program will not continue.")

    @classmethod
    def traitement(self):
        def real_traitement():
            self.progress.grid(row=7,column=0)
            self.progress.start()
            self.run["state"] = DISABLED
            self.run_tasks()
            self.run["state"] = NORMAL
            self.progress.stop()
            self.progress.grid_forget()
        threading.Thread(target=real_traitement).start()

    @classmethod
    def _quit(self): 
        self.my_logger.create_log(f"[user_interface] Program has been closed/terminated.", self.my_logger.get_logging_module().INFO)
        self.root.quit()  
        self.root.destroy()  
        exit() 
