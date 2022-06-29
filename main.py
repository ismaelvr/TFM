import constants as cons
import tkinter as tk
from operations.blake2 import BLAKE2
from tkinter import ttk
import ctypes

class App:
    def __init__(self, root = None):
        self.root = root
        self.root.title(cons.title)
        self.root.geometry(cons.screen_size)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.frame = ttk.Frame(self.root)
        self.main_menu = tk.Menu(self.root, tearoff=0)
        self.root.config(menu=self.main_menu)

        # Creating exit
        file_menu = tk.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Salir", command=self.root.quit)

        # Creating Operation menu
        operation_menu = tk.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="Operaciones", menu=operation_menu)
        operation_menu.add_command(label="BLAKE2", command=self.make_blake2)

        # Creating Help menu
        help_menu = tk.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Soporte teórico")

        # Creating Properties menu
        properties_menu = tk.Menu(self.main_menu)

        # Creating Algorithms menu
        encrypt_menu = tk.Menu(self.main_menu)

        self.frame.grid()

        ttk.Label(self.frame, text='Selecciona un algoritmo').grid()


    def make_blake2(self):
        self.blake2 = BLAKE2(master=self.root, app=self)
        self.frame.grid_forget()
        self.blake2.start_page()

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()