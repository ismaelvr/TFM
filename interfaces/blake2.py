import tkinter as tk
from PIL import ImageTk as itk
import constants as cons
from algorithms.blake2 import BLAKE2b
import binascii
import algorithms.b2_g as b2_g
import algorithms.b2_round as b2_r
import algorithms.b2_block as b2_b
import interfaces.tooltip as ttp

def create_frames(self):
    self.main_frame = tk.Frame(self.frame, highlightbackground="grey", highlightthickness=2)
    self.main_frame.pack(pady=15)

    self.new_windows_main_frame = tk.Frame(self.main_frame)

    self.reset_button = tk.Button(self.main_frame)
    self.reset_button.config(text="Reset", command=lambda: reset_all(self))
    self.reset_button.pack(pady=[15, 0])
    self.reset_button['state'] = tk.DISABLED

    self.message_frame = tk.Frame(self.main_frame)
    self.message_label = tk.Label(self.message_frame)
    self.message_label.config(text="Mensaje =")
    self.message_label.pack(side="left")
    self.message_entry = tk.Entry(self.message_frame, width=200)

    self.message_entry.pack(side="left")
    self.message_frame.pack(pady=15)

    self.hash_frame = tk.Frame(self.main_frame)
    self.hash_val_str = tk.StringVar()
    self.hash_label = tk.Label(self.hash_frame)
    self.hash_label.config(text="Hash =")
    self.hash_label.pack(side="left")
    self.hash_label_val = tk.Label(self.hash_frame, textvariable=self.hash_val_str)
    self.hash_label_val.pack(side="left")
    self.hash_frame.pack(pady=5)

    self.calc_hash_frame = tk.Frame(self.main_frame)
    self.calc_hash_button = tk.Button(self.calc_hash_frame)
    self.calc_hash_button.config(text="Listo", command=lambda: calc_hash(self))
    self.calc_hash_button.pack(pady=10)

    self.calc_hash_frame.pack()

def calc_hash(self):
    if (len(self.message_entry.get()) == 0):
        self.hash_val_str.set("El mensaje no puede estar vacio")
    else:
        self.v = [0]*16
        self.reset_button['state'] = tk.NORMAL
        self.calc_hash_button['state'] = tk.DISABLED

        BLOCKBYTES = 128
        message = self.message_entry.get().encode()
        self.N_BLOCKS = int(len(message) / BLOCKBYTES) + 1
        self.blocks = [b2_b.b2_block() for x in range(self.N_BLOCKS)]
        self.b2 = BLAKE2b(digest_size=64, vs = self.v, blocks_data = self.blocks)
        self.b2.update(message)
        digest = self.b2.final()
        self.blocks = self.b2.blocks_data
        self.v = self.b2.vs

        print(self.blocks[0].rs[0].gs[0].g_final_values[0])
        
        self.hs = self.b2.hs
        self.h_init = self.b2.h_init
        actual = binascii.hexlify(digest).decode()
        self.hash_val_str.set(actual)

        create_windows(self)

def reset_all(self):
    for widgets in self.new_windows_main_frame.winfo_children():
        widgets.destroy()
    self.reset_button['state'] = tk.DISABLED
    self.calc_hash_button['state'] = tk.NORMAL
    self.message_entry.delete(0, 'end')
    self.hash_val_str.set("")

def create_windows(self):
        create_IV_window(self, IVs = self.b2.IV)
        create_internal_state_window(self)
        create_blocks_window(self)
        create_sigma_window(self, sigma = self.b2.sigma)
        create_rounds_window(self)
        create_gs_window(self)
        create_teoric_window(self)

def create_teoric_window(self):
    self.teoricWindow = tk.Toplevel(self.new_windows_main_frame)
    self.teoricWindow.transient(self.main_frame)
    self.teoricWindow.title("Ayuda")
    self.teoricWindow.geometry(cons.teoric_window_size)
    self.teoricWindow.resizable(False, False)
    self.teoricWindow.attributes('-topmost',True)
    
    # img = itk.PhotoImage(file = "a.jpg")
    # canvas = tk.Canvas(self.teoricWindow, width=500, height=250)
    # canvas.imageList = []
    # canvas.pack()
    # canvas.create_image(0, 0, anchor="nw", image=img)
    # canvas.imageList.append(img)

    self.teoric_title_frame = tk.Frame(self.teoricWindow, pady = 10)

    self.teoric_title_val_str = tk.StringVar()
    self.teoric_title_label = tk.Label(self.teoric_title_frame, font='Helvetica 16 bold')
    self.teoric_title_label.config(text="Guía de uso")
    self.teoric_title_label.pack()
    self.teoric_title_frame.pack()

    self.teoric_text_frame = tk.Frame(self.teoricWindow)
    
    self.teoric_text__val_str = tk.StringVar()
    self.teoric_text_label = tk.Label(self.teoric_text_frame, font='Helvetica 13', wraplength=770)
    self.teoric_text_label.config(text="En la ventana de bloques puedes desplazarte a través de los bloques en caso de que haya más de uno. En la tabla h aparecen los valores de h al finalizar la ejecución de los pasos de ese bloque. Poniendo el cursor encima de uno de los elementos se puede ver los cálculos realizados para su obtención. Con el botón Hex/Dec puedes alternar entre los valores en hexadecimal o decimal.\n\n"
    "En la ventana de rondas puedes desplazarte dentro de cada una de las 12 rondas que se realizan en cada bloque. Además, puedes ver los valores de a, b, c y d obtenidos tras la ejecución de cada una de las 8 funciones G de la ronda actual. El texto en rojo indica cuales son los valores de la G actual.\n\n"
    "En la ventana de función G puedes desplazarte dentro de cada una de las 8 funciones G que se realizan en cada ronda y, a su vez, desplazarte dentro de cada uno de los 8 pasos que realizan en cada función G. En los pasos en los que se realizan operaciones xor se puede ver el cálculo poniendo el ratón encima.\n\n"
    "En la ventana sigma se pueden ver los valores de la tabla sigma. Si se mantiene el cursor encima de uno de los elementos de la tabla se puede ver el valor que corresponde del m de ese bloque\n\n"
    "En la ventana estado interno se pueden ver en rojo los valores que están siendo usados en la función G actual. Si se mantiene el cursor encima de uno de los elementos de la tabla se puede ver su valor actual.")
    self.teoric_text_label.pack()
    self.teoric_text_frame.pack()

    self.teoric_text_frame2 = tk.Frame(self.teoricWindow, pady = 5)

def create_sigma_window(self, sigma):
    self.sigmaWindow = tk.Toplevel(self.new_windows_main_frame)
    self.sigmaWindow.transient(self.main_frame)
    self.sigmaWindow.title("Tabla sigma")
    self.sigmaWindow.geometry(cons.sigma_window_size)
    self.sigmaWindow.resizable(False, False)
    self.sigmaWindow.attributes('-topmost',True)
    total_rows = len(sigma)
    total_columns = len(sigma[0])

    self.entry_grid_sigma = [[0 for y in range(total_columns)] for x in range(total_rows-2)]
    for i in range(total_rows-2):
        for j in range(total_columns):

            self.e = tk.Entry(self.sigmaWindow, justify=tk.CENTER, width=2, font=('Arial',11,'bold'))
            self.e.grid(row=i, column=j)
            self.e.insert(tk.END, sigma[i][j])
            self.entry_grid_sigma[i][j] = self.e
            self.e.config( state="readonly")
    update_sigma_window(self, n_round = 0, mi = self.actual_block_rounds[0].gs[0].m_pos[0], mj = self.actual_block_rounds[0].gs[0].m_pos[1])
    
def create_IV_window(self, IVs):
    self.IVWindow = tk.Toplevel(self.new_windows_main_frame)
    self.IVWindow.transient(self.main_frame)
    self.IVWindow.title("Tabla IVs")
    self.IVWindow.geometry(cons.IV_window_size)
    self.IVWindow.resizable(False, False)
    self.IVWindow.attributes('-topmost',True)
    total_rows = len(IVs)
    self.entry_grid_IV = [0 for x in range(total_rows)]
    for i in range(total_rows):
        self.e = tk.Entry(self.IVWindow, justify=tk.CENTER, width=20, font=('Arial',11,'bold'))
        self.e.grid(row=i, column=0)
        self.e.insert(tk.END, hex(IVs[i]))
        self.entry_grid_IV[i] = self.e
        self.e.config( state="readonly")

def create_rounds_window(self):
    self.actual_round = 1
    self.roundsWindow = tk.Toplevel(self.new_windows_main_frame)
    self.roundsWindow.transient(self.main_frame)
    self.roundsWindow.title("Tabla Rondas")
    self.roundsWindow.geometry(cons.rounds_window_size)
    self.roundsWindow.resizable(False, False)
    self.roundsWindow.attributes('-topmost',True)

    self.rounds_text_frame = tk.Frame(self.roundsWindow)

    self.previous_round_button = tk.Button(self.rounds_text_frame)
    self.previous_round_button.config(text="Anterior", command=lambda: b2_r.previous_round(self))
    self.previous_round_button['state'] = tk.DISABLED
    self.previous_round_button.pack(padx=15, side= tk.LEFT)

    self.round_val_str = tk.StringVar()
    self.rounds_label = tk.Label(self.rounds_text_frame, font='Helvetica 16 bold', textvariable=self.round_val_str)
    self.rounds_label.config(text="Round: "+ str(self.round_val_str))
    self.rounds_label.pack(side = tk.LEFT)

    self.next_round_button = tk.Button(self.rounds_text_frame)
    self.next_round_button.config(text="Siguiente", command=lambda: b2_r.next_round(self))
    self.next_round_button.pack(padx=15, side=tk.LEFT)

    self.rounds_text_frame.pack()

    self.rounds_frame = tk.Frame(self.roundsWindow)
    b2_r.load_round(self, rounds = self.actual_block_rounds, n_round = self.actual_round)

def create_gs_window(self):
    self.actual_g = 0
    self.actual_step = 1

    self.gsWindow = tk.Toplevel(self.new_windows_main_frame)
    self.gsWindow.transient(self.main_frame)
    self.gsWindow.title("Tabla función G")
    self.gsWindow.geometry(cons.gs_window_size)
    self.gsWindow.resizable(False, False)
    self.gsWindow.attributes('-topmost',True)

    self.gs_text_frame = tk.Frame(self.gsWindow)

    self.previous_step_button = tk.Button(self.gs_text_frame)
    self.previous_step_button.config(text="Paso anterior", command=lambda: b2_g.previous_step(self))
    self.previous_step_button['state'] = tk.DISABLED
    self.previous_step_button.pack(side= tk.LEFT)

    self.previous_g_button = tk.Button(self.gs_text_frame)
    self.previous_g_button.config(text="G anterior", command=lambda: b2_g.previous_g(self))
    self.previous_g_button['state'] = tk.DISABLED
    self.previous_g_button.pack(padx=5, side= tk.LEFT)

    self.gs_val_str = tk.StringVar()
    self.gs_val_str.set("G" + str(self.actual_g))
    self.gs_label = tk.Label(self.gs_text_frame, font='Helvetica 16 bold', textvariable=self.gs_val_str)
    self.gs_label.pack(side = tk.LEFT)

    self.next_g_button = tk.Button(self.gs_text_frame)
    self.next_g_button.config(text="G siguiente", command=lambda: b2_g.next_g(self))
    self.next_g_button.pack(padx=5, side=tk.LEFT)

    self.next_step_button = tk.Button(self.gs_text_frame)
    self.next_step_button.config(text="Paso siguiente", command=lambda: b2_g.next_step(self))
    self.next_step_button.pack(side=tk.LEFT)

    self.gs_text_frame.pack(pady = 10)

    self.gs_frame = tk.Frame(self.gsWindow)
    self.gs_act_vals_frame = tk.Frame(self.gsWindow)
    self.gs_act_vals_str = tk.StringVar()
    self.gs_act_vals_label = tk.Label(self.gs_act_vals_frame, font='Helvetica 16 bold', textvariable=self.gs_act_vals_str)
    b2_g.load_g(self, ng = self.actual_g)

    self.gs_act_vals_frame.pack(pady = 10)

def create_internal_state_window(self):
    self.vsWindow = tk.Toplevel(self.new_windows_main_frame)
    self.vsWindow.transient(self.main_frame)
    self.vsWindow.title("Tabla estado interno")
    self.vsWindow.geometry(cons.internal_state_window_size)
    self.vsWindow.resizable(False, False)
    self.vsWindow.attributes('-topmost',True)

    self.vs_text_frame = tk.Frame(self.vsWindow)

    self.vs_text_frame.pack()

    self.vs_frame = tk.Frame(self.vsWindow)
    b2_g.load_vs(self)

def create_blocks_window(self):
    self.hex_on = False 
    self.actual_block = 1
    self.actual_block_rounds = [self.blocks[self.actual_block - 1].rs[x] for x in range(cons.n_rounds)] 
    self.hsWindow = tk.Toplevel(self.new_windows_main_frame)
    self.hsWindow.transient(self.main_frame)
    self.hsWindow.title("Bloques")
    self.hsWindow.geometry(cons.blocks_window_size)
    self.hsWindow.resizable(False, False)
    self.hsWindow.attributes('-topmost',True)

    self.blocks_text_frame = tk.Frame(self.hsWindow)

    self.previous_block_button = tk.Button(self.blocks_text_frame)
    self.previous_block_button.config(text="Bloque anterior", command=lambda: b2_b.previous_block(self))
    self.previous_block_button['state'] = tk.DISABLED
    self.previous_block_button.pack(padx=15, side= tk.LEFT)

    self.block_val_str = tk.StringVar()
    self.block_val_str.set("Bloque: " + str(self.actual_block) + "/" +str(self.N_BLOCKS))
    self.blocks_label = tk.Label(self.blocks_text_frame, font='Helvetica 16 bold', textvariable=self.block_val_str)
    self.blocks_label.config(text="Bloque: "+ str(self.block_val_str))
    self.blocks_label.pack(side = tk.LEFT)

    self.next_block_button = tk.Button(self.blocks_text_frame)
    self.next_block_button.config(text="Bloque siguiente", command=lambda: b2_b.next_block(self))
    self.next_block_button.pack(padx=15, side=tk.LEFT)
    if self.N_BLOCKS == 1:
        self.next_block_button['state'] = tk.DISABLED

    self.blocks_text_frame.pack()

    self.hs_text_frame = tk.Frame(self.hsWindow)

    self.hs_label = tk.Label(self.hs_text_frame, font='Helvetica 11 bold')
    if self.actual_block == self.N_BLOCKS:
            self.hs_label.config(text="hash final:")
    else: 
        self.hs_label.config(text="hash al finalizar el bloque actual:")
    self.hs_label.pack(side = tk.LEFT)

    self.hs_text_frame.pack()

    self.hs_frame = tk.Frame(self.hsWindow)
    b2_b.load_hs(self, hs = self.hs[0], n_block = self.actual_block)
    

    self.hs_frame.pack()

    self.hex_block_button = tk.Button(self.hsWindow)
    self.hex_block_button.config(text="Hex/Dec", command=lambda: b2_b.hex_dec(self))
    self.hex_block_button.pack(pady=5)

def update_internal_state_window(self, ng):
    
    for i in range(len(self.entry_grid_vs)):
        for j in range(len(self.entry_grid_vs[0])):   
            self.entry_grid_vs[i][j].config(fg="black")

    if self.actual_g < 4:
        for pos in range(4):
            self.entry_grid_vs[ng][pos].config(fg="red")
            
    if self.actual_g >= 4:
        for pos in range(4):
            self.entry_grid_vs[(ng + pos) % 4][pos].config(fg="red")

def update_sigma_window(self, n_round, mi , mj):
    
    for i in range(len(self.entry_grid_sigma)):
        for j in range(len(self.entry_grid_sigma[0])):   
            self.entry_grid_sigma[i][j].config(fg="black")
            
    for i in range(len(self.entry_grid_sigma)):
        k = 0
        for j in range(0, len(self.entry_grid_sigma[0]), 2):
            self.entry_grid_sigma[i][j].config(fg="black")
            self.e_ttp = ttp.ToolTip(self.entry_grid_sigma[i][j], self.actual_block_rounds[0].gs[k].m[0])
            self.e_ttp = ttp.ToolTip(self.entry_grid_sigma[i][j + 1], self.actual_block_rounds[0].gs[k].m[1])   
            k = k + 1 
    self.entry_grid_sigma[(n_round - 1) % 10][mi].config(fg="red")
    self.entry_grid_sigma[(n_round - 1) % 10][mj].config(fg="red")

