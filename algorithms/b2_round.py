import algorithms.b2_g as b2_g
import interfaces.blake2 as b2_int
import constants as cons
import tkinter as tk

class b2_round:
    
    def __init__(self):
        self.gs = [b2_g.b2_g() for x in range(cons.n_gs)]

def previous_round(self):
    if self.actual_round > 1:
        self.actual_round = self.actual_round - 1
        self.next_round_button['state'] = tk.NORMAL
        self.next_step_button['state'] = tk.NORMAL
        self.previous_step_button['state'] = tk.DISABLED
        self.next_g_button['state'] = tk.NORMAL
        self.previous_g_button['state'] = tk.DISABLED
        load_round(self, rounds = self.actual_block_rounds, n_round = self.actual_round)
        self.actual_g = 0
        b2_g.load_g(self, ng = self.actual_g)
    if self.actual_round == 1:
        self.previous_round_button['state'] = tk.DISABLED

def next_round(self):
    if self.actual_round < cons.n_rounds:
        self.actual_round = self.actual_round + 1
        self.previous_round_button['state'] = tk.NORMAL
        self.next_step_button['state'] = tk.NORMAL
        self.previous_step_button['state'] = tk.DISABLED
        self.next_g_button['state'] = tk.NORMAL
        self.previous_g_button['state'] = tk.DISABLED
        load_round(self, rounds = self.actual_block_rounds, n_round = self.actual_round)
        self.actual_g = 0
        b2_g.load_g(self, ng = self.actual_g)
    if self.actual_round == cons.n_rounds:
        self.next_round_button['state'] = tk.DISABLED

def load_round(self, rounds, n_round):
    self.actual_g = 0
    self.round_val_str.set("Ronda: " + str(self.actual_round) + "/" +str(cons.n_rounds))

    b2_int.update_internal_state_window(self, ng = self.actual_g)
    b2_int.update_sigma_color(self, mi = self.actual_block_rounds[n_round - 1].gs[self.actual_g].m_pos[0], mj = self.actual_block_rounds[n_round - 1].gs[self.actual_g].m_pos[1])
    total_rows = len(rounds[n_round - 1].gs)
    total_columns = len(rounds[n_round - 1].gs[0].g_final_values)
    self.entry_grid_round_gs = [[rounds[n_round - 1].gs[x].g_final_values[y] for x in range(total_rows)] for y in range(total_columns)]
    for i in range(total_rows):
            for j in range(total_columns):
                if i == 0:
                    self.e = tk.Entry(self.rounds_frame, justify=tk.CENTER, width=20, font=('Consolas',11,'bold'))
                    self.e.grid(row=i, column=j+1)
                    if j == 0:
                        self.e.insert(tk.END, "a")
                    if j == 1:
                        self.e.insert(tk.END, "b")
                    if j == 2:
                        self.e.insert(tk.END, "c")
                    if j == 3:
                        self.e.insert(tk.END, "d")
                    self.e.config( state="readonly")

                if j == 0:
                    self.e = tk.Entry(self.rounds_frame, justify=tk.CENTER, width=3, font=('Consolas',11,'bold'))
                    self.e.grid(row=i+1, column=j)
                    self.e.insert(tk.END, "G"+str(i))
                    self.e.config( state="readonly")

                self.e = tk.Entry(self.rounds_frame, justify=tk.CENTER, width=20, font=('Consolas',11,'bold'))
                self.e.grid(row=i+1, column=j+1)
                self.e.insert(tk.END, rounds[n_round - 1].gs[i].g_final_values[j])
                self.entry_grid_round_gs[j][i] = self.e
                self.e.config( state="readonly")
    self.rounds_frame.pack()