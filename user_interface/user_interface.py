import os
import time
import threading
from configparser import ConfigParser
from system_logger.system_logger import system_logger
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import *
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
            self.root.iconbitmap(os.path.join(os.getcwd(), self.config.get("USER_INTERFACE","ICON")))
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
        a = Label(self.root ,text = "Target Directory").grid(row = 0,column = 0, padx=5, pady=5)
        b = Label(self.root ,text = "Regular Expression").grid(row = 1,column = 0, padx=5, pady=5)
        c = Label(self.root ,text = "Save Location").grid(row = 2, column = 0, padx=5, pady=5)
        d = Label(self.root ,text = "Function Order").grid(row = 2, column = 0, padx=5, pady=5)
        a1 = Entry(self.root).grid(row = 0,column = 1, padx=5, pady=5)
        b1 = Entry(self.root).grid(row = 1,column = 1, padx=5, pady=5)
        c1 = Entry(self.root).grid(row = 2,column = 1, padx=5, pady=5)
        self.run = Button(self.root, text="Run", command=self.traitement)
        self.run.grid(row = 5, column=1, padx=5, pady=5)
        self.progress = Progressbar(self.root, orient = HORIZONTAL,length = 100, mode = 'indeterminate')
        menu_bar.add_cascade(label="Options", menu=file_menu) 
        menu_bar.add_cascade(label="Help", menu=help_menu) 

    @classmethod
    def help_window(self):
        messagebox.showinfo(f'[v{self.config.get("SYSTEM","VERSION")}] About', f'''Hi guys, this is a simple app which helps you organize your files. The app has been tested and is working fine. IF YOU MESS UP YOUR FILES, IT IS NOT MY RESPONSIBILITY. Test this app on a prototype/test directory and then use it on your files.\nMade with love, roganjosh, sambar, idli, pani puri and butter chicken in India.''')
   
    @classmethod
    def run_tasks(self):
        print("running...")
        time.sleep(2)

    @classmethod
    def traitement(self):
        def real_traitement():
            self.progress.grid(row=5,column=0)
            self.progress.start()
            self.run["state"] = DISABLED
            self.run_tasks()
            self.run["state"] = NORMAL
            self.progress.stop()
            self.progress.grid_forget()
        threading.Thread(target=real_traitement).start()

    @classmethod
    def _quit(self):  
        self.root.quit()  
        self.root.destroy()  
        exit() 
