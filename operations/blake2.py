import tkinter as tk
import constants as cons
from interfaces.blake2 import *

class BLAKE2:
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.app.frame.grid_forget()
        self.frame = tk.Frame(self.master)
        self.title = tk.Label(self.frame, text='BLAKE2', font='Consolas 16 bold')
        self.title.pack(fill="x")
    
        self.message = b"Mensaje" # Texto a encriptar
        self.hash = None # Texto encriptado
        self.teoricWindow = None
        
        create_frames(self)
       
    def start_page(self):
        self.frame.grid(column=0, row=0, sticky="NWES")

    def c_teoric_window(self):
        create_teoric_window(self)