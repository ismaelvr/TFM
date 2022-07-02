from unicodedata import decimal
import interfaces.blake2 as b2_int
import algorithms.b2_round as b2_r
import algorithms.b2_g as b2_g
import interfaces.tooltip as ttp
import tkinter as tk
import constants as cons
import struct
import binascii

class b2_block:
    
    def __init__(self):
        self.rs = [b2_r.b2_round() for x in range(cons.n_rounds)] 
        self.v_fin = [0]*16
    
def previous_block(self):
    if self.actual_block > 1:
        self.actual_round = 1
        self.actual_g = 0
        self.actual_step = 1
        self.actual_block = self.actual_block - 1
        self.block_val_str.set("Bloque: " + str(self.actual_block) + "/" +str(self.N_BLOCKS))
        self.next_block_button['state'] = tk.NORMAL
        self.next_step_button['state'] = tk.NORMAL
        self.previous_step_button['state'] = tk.DISABLED
        self.next_g_button['state'] = tk.NORMAL
        self.previous_g_button['state'] = tk.DISABLED
        self.actual_hs = self.hs[self.actual_block - 1]
        self.actual_block_rounds = [self.blocks[self.actual_block - 1].rs[x] for x in range(cons.n_rounds)] 
        b2_r.load_round(self, rounds = self.actual_block_rounds, n_round = self.actual_round)
        b2_g.load_g(self, ng = self.actual_g)
        if self.actual_block == self.N_BLOCKS:
            self.hs_label.config(text="hash final:")
        else:
            self.hs_label.config(text="hash al finalizar el bloque actual:")
        b2_int.update_sigma_window(self, mi = self.actual_block_rounds[self.actual_round - 1].gs[0].m_pos[0], mj = self.actual_block_rounds[0].gs[0].m_pos[1])
        b2_int.update_sigma_color(self, mi = self.actual_block_rounds[self.actual_round - 1].gs[0].m_pos[0], mj = self.actual_block_rounds[0].gs[0].m_pos[1])

        load_hs(self, hs = self.actual_hs, n_block = self.actual_block)
        self.actual_g = 0
        self.hs_frame.pack()
    if self.actual_block == 1:
        self.previous_block_button['state'] = tk.DISABLED

def next_block(self):
    if self.actual_block < self.N_BLOCKS:
        self.actual_round = 1
        self.actual_g = 0
        self.actual_step = 1
        self.actual_block = self.actual_block + 1
        self.block_val_str.set("Bloque: " + str(self.actual_block) + "/" +str(self.N_BLOCKS))
        self.previous_block_button['state'] = tk.NORMAL
        self.previous_round_button['state'] = tk.DISABLED
        self.previous_step_button['state'] = tk.DISABLED
        self.next_step_button['state'] = tk.NORMAL
        self.next_round_button['state'] = tk.NORMAL
        self.next_g_button['state'] = tk.NORMAL
        self.previous_g_button['state'] = tk.DISABLED
        self.actual_hs = self.hs[self.actual_block - 1]
        self.actual_block_rounds = [self.blocks[self.actual_block - 1].rs[x] for x in range(cons.n_rounds)] 
        b2_r.load_round(self, rounds = self.actual_block_rounds, n_round = self.actual_round)
        b2_g.load_g(self, ng = self.actual_g)
        if self.actual_block == self.N_BLOCKS:
            self.hs_label.config(text="hash final:")
        else:
            self.hs_label.config(text="hash al finalizar el bloque actual:")
        b2_int.update_sigma_window(self, mi = self.actual_block_rounds[self.actual_round - 1].gs[0].m_pos[0], mj = self.actual_block_rounds[0].gs[0].m_pos[1])
        b2_int.update_sigma_color(self, mi = self.actual_block_rounds[self.actual_round - 1].gs[0].m_pos[0], mj = self.actual_block_rounds[0].gs[0].m_pos[1])

        load_hs(self, hs = self.actual_hs, n_block = self.actual_block)
        self.hs_frame.pack()
        self.actual_g = 0
    if self.actual_block == self.N_BLOCKS:
        self.next_block_button['state'] = tk.DISABLED

def ttp_format(self, hs, v, x):
  
    v0 = b2_g.separate_bytes(v[x])
    v1 = b2_g.separate_bytes(v[x+8])
    h_fin = b2_g.separate_bytes(hs[x])
    if self.actual_block == 1:
        h_ini = self.h_init[x]
    else:
        h_ini = self.hs[self.actual_block - 2][x]

    h_ini = b2_g.separate_bytes(h_ini)
    if x < 2:
        self.e_ttp = ttp.ToolTip(self.e, "Cálculo realizado:\nv" + str(x) + ":  " + str(v0) + "\nv" + str(x+8) + ":  " + str(v1) + "\nh" + str(x) + ":  " + str(h_ini) + "\n"
        "------------------------------------------------------------------------------------------------------------------\n⊕:    "+ str(h_fin), width=65, height=8)
    else:
        self.e_ttp = ttp.ToolTip(self.e, "Cálculo realizado:\nv" + str(x) + ":  " + str(v0) + "\nv" + str(x+8) + ":" + str(v1) + "\nh" + str(x) + ":  " + str(h_ini) + "\n"
        "------------------------------------------------------------------------------------------------------------------\n⊕:    "+ str(h_fin), width=65, height=8)

def load_hs(self, hs, n_block):

    total_rows = len(hs)
    self.entry_grid_hs = [0 for x in range(total_rows)]
    for i in range(total_rows):
        self.e = tk.Entry(self.hs_frame, justify=tk.CENTER, width=3, font=('Consolas',11,'bold'))
        self.e.grid(row=i, column = 0)
        self.e.insert(tk.END, "h"+ str(i))
        self.e.config( state="readonly")
        self.e = tk.Entry(self.hs_frame, justify=tk.CENTER, width=20, font=('Consolas',11,'bold'))
        ttp_format(self, hs, self.b2.v_fin[n_block - 1], x = i)

        self.e.grid(row=i, column = 1)
        if self.hex_on == True:
            val = struct.pack('<Q', hs[i])
            val = binascii.hexlify(val)
            self.e.insert(tk.END, val)
        else:
            self.e.insert(tk.END, hs[i])

        self.entry_grid_hs[i] = self.e
        self.e.config( state="readonly")

def hex_dec(self):
    self.hex_on = not self.hex_on
    load_hs(self, self.hs[self.actual_block - 1], self.actual_block)
