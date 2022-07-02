import constants as cons
import tkinter as tk
from operations.blake2 import BLAKE2
from tkinter import ttk

class App:
    def __init__(self, root = None):
        self.root = root
        self.root.state('zoomed')
        self.root.title(cons.title)
        self.root.geometry(cons.screen_size)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.frame = ttk.Frame(self.root)
        self.main_menu = tk.Menu(self.root, tearoff=0)
        self.root.config(menu=self.main_menu)

        self.file_menu = tk.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="Archivo", menu=self.file_menu)
        self.file_menu.add_command(label="Salir", command=self.root.quit)

        self.operation_menu = tk.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="Operaciones", menu=self.operation_menu)
        self.operation_menu.add_command(label="BLAKE2", command=self.make_blake2)

        self.help_menu = tk.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="Ayuda", menu=self.help_menu)

        ttk.Label(self.frame, text='Selecciona un algoritmo').grid()

        self.frame.grid()

    def make_blake2(self):
        self.blake2 = BLAKE2(master=self.root, app=self)
        self.blake2.start_page()
        self.help_menu.add_command(label="Guía de uso", command = self.blake2.c_teoric_window)

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()