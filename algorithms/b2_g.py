import tkinter as tk
import interfaces.tooltip as ttp
import interfaces.blake2 as b2_int
import constants as cons

class b2_g:

    def __init__(self):

        self.g_init_values = [0]*4
        self.g_mid_values = [0]*4
        self.g_final_values = [0]*4
        
        self.m_pos = [0]*2
        self.m = [0]*2
       
def load_g(self, ng):
    self.gs_val_str.set("G" + str(self.actual_g) + "/" +str(cons.n_gs - 1))

    for widgets in self.gs_frame.winfo_children():
        widgets.destroy()
    
    self.actual_step = 1

    for i in range(len(self.entry_grid_round_gs)):
        for j in range(len(self.entry_grid_round_gs[0])):   
            self.entry_grid_round_gs[i][j].config(fg="black")
    
    for x in range(4):
        self.entry_grid_round_gs[x][ng].config(fg="red")
    
    load_step(self, gs = self.actual_block_rounds[self.actual_round - 1].gs[self.actual_g])
   
    self.gs_frame.pack()

def separate_bytes(data):
    result = bin(data)[2:]
    if len(result) < 64:
        result = ("0" * (64 - len(result))) + result
    result = " ".join([result[i:i+8] for i in range(0, len(result), 8)])
    return result


def ttp_format(self, op1, op2, res, val1, val2):
    op1_f = separate_bytes(op1)
    op2_f = separate_bytes(op2)
    
    xor = op1 ^ op2

    xor = separate_bytes(int(xor))
    res_f = separate_bytes(res)
    ttp_str = "Calculos de este paso:\n"+ val1 + ":   " + op1_f + "\n"+ val2 + ":   " + op2_f + "\n------------------------------------------------------------------------------------------------------------------\n⊕:   " + str(xor) + "\n------------------------------------------------------------------------------------------------------------------\n≫: " + res_f
    self.step_result_label_ttp = ttp.ToolTip(self.step_result_label, ttp_str, width=65, height=8)
    self.step_label_ttp = ttp.ToolTip(self.step_label, ttp_str, width=65, height=8)

def update_vs(self, ng, list):

    if self.actual_g < 4:
        for pos in range(4):
            self.entry_grid_vs_ttp[ng][pos].update_text(text = list[pos])
            
    if self.actual_g >= 4:
        for pos in range(4):
            self.entry_grid_vs_ttp[(ng + pos) % 4][pos].update_text(text = list[pos])


def load_step(self, gs):
    for widgets in self.gs_frame.winfo_children():
        widgets.destroy()
    self.step_text_frame = tk.Frame(self.gs_frame,  highlightbackground="grey", highlightthickness=2)
    self.step_val_str = tk.StringVar()
    self.step_label = tk.Label(self.step_text_frame, font='Helvetica 16 bold', textvariable=self.step_val_str)
    self.step_result_text_frame = tk.Frame(self.gs_frame)
    self.step_result_val_str = tk.StringVar()
    self.step_result_label = tk.Label(self.step_result_text_frame, font='Helvetica 16 bold', textvariable=self.step_result_val_str)

    if self.actual_step == 1:

        self.step_val_str.set("Paso 1/8: a ← a + b + mi")
        self.step_label.pack()
        self.step_text_frame.pack(pady = 10)
        
        self.step_result_val_str.set("Paso 1: " + str(gs.g_mid_values[0]) + " ← " + str(gs.g_init_values[0]) + " + " + str(gs.g_init_values[1]) + " + " + str(gs.m[0]))

        update_vs(self, ng = self.actual_g, list = [gs.g_mid_values[0], gs.g_init_values[1], gs.g_init_values[2], gs.g_init_values[3]])
        
        self.step_result_label.pack()
        self.step_result_text_frame.pack()

        self.gs_act_vals_str.set("Valores actuales: \na: " + str(gs.g_mid_values[0]) + " ← " + str(gs.g_init_values[0]) + " \n"
        "b: " + str(gs.g_init_values[1]) + " \nc: " + str(gs.g_init_values[2]) + " \nd: " + str(gs.g_init_values[3]))

    elif self.actual_step == 2:

        self.step_val_str.set("Paso 2/8: d ← (d ⊕ a) ≫ 32")
        self.step_label.pack()
        self.step_text_frame.pack(pady = 10)

        self.step_result_val_str.set("Paso 2: " + str(gs.g_mid_values[3]) + " ← (" + str(gs.g_init_values[3]) + " ⊕ " + str(gs.g_mid_values[0]) + ") ≫ 32 ")

        update_vs(self, ng = self.actual_g, list = [gs.g_mid_values[0], gs.g_init_values[1], gs.g_init_values[2], gs.g_mid_values[3]])
        
        ttp_format(self, gs.g_init_values[3], gs.g_mid_values[0], gs.g_mid_values[3], "d", "a")
      
        self.step_result_label.pack()
        self.step_result_text_frame.pack()

        self.gs_act_vals_str.set("Valores actuales: \na: " + str(gs.g_mid_values[0]) + "\n"
        "b: " + str(gs.g_init_values[1]) + " \nc: " + str(gs.g_init_values[2]) + " \nd: " + str(gs.g_mid_values[3]) + "←" + str(gs.g_init_values[3]))
    
    elif self.actual_step == 3:

        self.step_val_str.set("Paso 3/8: c ← c + d")
        self.step_label.pack()
        self.step_text_frame.pack(pady = 10)

        self.step_result_val_str.set("Paso 3: " + str(gs.g_mid_values[2]) + " ← " + str(gs.g_init_values[2]) + " + " + str(gs.g_mid_values[3]))

        update_vs(self, ng = self.actual_g, list = [gs.g_mid_values[0], gs.g_init_values[1], gs.g_mid_values[2], gs.g_mid_values[3]])

        self.step_result_label.pack()
        self.step_result_text_frame.pack()

        self.gs_act_vals_str.set("Valores actuales: \na: " + str(gs.g_mid_values[0]) + "\n"
        "b: " + str(gs.g_init_values[1]) + " \nc: " + str(gs.g_mid_values[2]) + " ← " + str(gs.g_init_values[2]) + " \nd: " + str(gs.g_mid_values[3]))   
    
    elif self.actual_step == 4:

        self.step_val_str.set("Paso 4/8: b ← (b ⊕ c) ≫ 24")
        self.step_label.pack()
        self.step_text_frame.pack(pady = 10)

        self.step_result_val_str.set("Paso 4: " + str(gs.g_mid_values[1]) + " ← (" + str(gs.g_init_values[1]) + " ⊕ " + str(gs.g_mid_values[2]) + ") ≫ 24")
    
        update_vs(self, ng = self.actual_g, list = [gs.g_mid_values[0], gs.g_mid_values[1], gs.g_mid_values[2], gs.g_mid_values[3]])

        ttp_format(self, gs.g_init_values[1], gs.g_mid_values[2], gs.g_mid_values[1], "b", "c")

        self.step_result_label.pack()
        self.step_result_text_frame.pack()

        self.gs_act_vals_str.set("Valores actuales: \na: " + str(gs.g_mid_values[0]) + "\n"
        "b: " + str(gs.g_mid_values[1]) + " ← " + str(gs.g_init_values[1]) + " \nc: " + str(gs.g_mid_values[2]) + " \nd: " + str(gs.g_mid_values[3]))     

    elif self.actual_step == 5:

        self.step_val_str.set("Paso 5/8: a ← a + b + mj")
        self.step_label.pack()
        self.step_text_frame.pack(pady = 10)

        self.step_result_val_str.set("Paso 5: " + str(gs.g_final_values[0]) + " ← " + str(gs.g_mid_values[0]) + " + " + str(gs.g_mid_values[1]) + " + " + str(gs.m[1]))

        update_vs(self, ng = self.actual_g, list = [gs.g_final_values[0], gs.g_mid_values[1], gs.g_mid_values[2], gs.g_mid_values[3]])

        self.step_result_label.pack()
        self.step_result_text_frame.pack()

        self.gs_act_vals_str.set("Valores actuales: \na: " + str(gs.g_final_values[0]) + " ← " + str(gs.g_mid_values[0]) + " \n"
        "b: " + str(gs.g_mid_values[1]) + " \nc: " + str(gs.g_mid_values[2]) + " \nd: " + str(gs.g_mid_values[3]))   

    elif self.actual_step == 6:

        self.step_val_str.set("Paso 6/8: d ← (d ⊕ a) ≫ 16")
        self.step_label.pack()
        self.step_text_frame.pack(pady = 10)

        self.step_result_val_str.set("Paso 6: " + str(gs.g_final_values[3]) + " ← (" + str(gs.g_mid_values[3]) + " ⊕ " + str(gs.g_final_values[0]) + ") ≫ 16")

        update_vs(self, ng = self.actual_g, list = [gs.g_final_values[0], gs.g_mid_values[1], gs.g_mid_values[2], gs.g_final_values[3]])

        ttp_format(self, gs.g_mid_values[3], gs.g_final_values[0], gs.g_final_values[3], "d", "a")

        self.step_result_label.pack()
        self.step_result_text_frame.pack()

        self.gs_act_vals_str.set("Valores actuales: \na: " + str(gs.g_final_values[0]) + "\n"
        "b: " + str(gs.g_mid_values[1]) + " \nc: " + str(gs.g_mid_values[2]) + " \nd: " + str(gs.g_final_values[3]) + " ← " + str(gs.g_mid_values[3]))   

    elif self.actual_step == 7:

        self.step_val_str.set("Paso 7/8: c ← c + d")
        self.step_label.pack()
        self.step_text_frame.pack(pady = 10)

        self.step_result_val_str.set("Paso 7: " + str(gs.g_final_values[2]) + " ← " + str(gs.g_mid_values[2]) + " + " + str(gs.g_final_values[3]))

        update_vs(self, ng = self.actual_g, list = [gs.g_final_values[0], gs.g_mid_values[1], gs.g_final_values[2], gs.g_final_values[3]])

        self.step_result_label.pack()
        self.step_result_text_frame.pack()

        self.gs_act_vals_str.set("Valores actuales: \na: " + str(gs.g_final_values[0]) + "\n"
        "b: " + str(gs.g_mid_values[1]) + " \nc: " + str(gs.g_final_values[2]) + " ← " + str(gs.g_mid_values[2]) + " \nd: " + str(gs.g_final_values[3]))   

    elif self.actual_step == 8:

        self.step_val_str.set("Paso 8/8: b ← (b ⊕ c) ≫ 63")
        self.step_label.pack()
        self.step_text_frame.pack(pady = 10)

        self.step_result_val_str.set("Paso 8: " + str(gs.g_final_values[1]) + " ← (" + str(gs.g_mid_values[1]) + " ⊕ " + str(gs.g_final_values[2]) + ") ≫ 63")

        update_vs(self, ng = self.actual_g, list = [gs.g_final_values[0], gs.g_final_values[1], gs.g_final_values[2], gs.g_final_values[3]])

        ttp_format(self, gs.g_mid_values[1], gs.g_final_values[2], gs.g_final_values[1], "b", "c")

        self.step_result_label.pack()
        self.step_result_text_frame.pack()

        self.gs_act_vals_str.set("Valores actuales: \na: " + str(gs.g_final_values[0]) + "\n"
        "b: " + str(gs.g_final_values[1]) + " ← " + str(gs.g_mid_values[1]) + " \nc: " + str(gs.g_final_values[2]) + " \nd: " + str(gs.g_final_values[3]))   

    self.gs_act_vals_label.pack(side = tk.LEFT)

def previous_g(self):
    if self.actual_g > 0:
        self.actual_g = self.actual_g - 1
        self.actual_step = 1
        self.next_g_button['state'] = tk.NORMAL
        self.previous_step_button['state'] = tk.DISABLED
        self.next_step_button['state'] = tk.NORMAL
        load_g(self, ng = self.actual_g)
        b2_int.update_internal_state_window(self, ng = self.actual_g)
        b2_int.update_sigma_window(self, n_round = self.actual_round, mi = self.actual_block_rounds[self.actual_round - 1].gs[self.actual_g].m_pos[0], mj = self.actual_block_rounds[self.actual_round - 1].gs[self.actual_g].m_pos[1])
    
    if self.actual_g == 0:
        self.previous_g_button['state'] = tk.DISABLED

def next_g(self):
    if self.actual_g < cons.n_gs - 1:
        self.actual_g = self.actual_g + 1
        self.actual_step = 1
        self.previous_g_button['state'] = tk.NORMAL
        self.previous_step_button['state'] = tk.DISABLED
        self.next_step_button['state'] = tk.NORMAL
        load_g(self, ng = self.actual_g)
        b2_int.update_internal_state_window(self, ng = self.actual_g)
        b2_int.update_sigma_window(self, n_round = self.actual_round, mi = self.actual_block_rounds[self.actual_round - 1].gs[self.actual_g].m_pos[0], mj = self.actual_block_rounds[self.actual_round - 1].gs[self.actual_g].m_pos[1])
    if self.actual_g == cons.n_gs - 1:
        self.next_g_button['state'] = tk.DISABLED
 
def previous_step(self):
    if self.actual_step > 1:
        self.actual_step = self.actual_step - 1
        self.next_step_button['state'] = tk.NORMAL
        load_step(self, gs = self.actual_block_rounds[self.actual_round - 1].gs[self.actual_g])
    if self.actual_step == 1:
        self.previous_step_button['state'] = tk.DISABLED

def next_step(self):
    if self.actual_step < cons.n_step:
        self.actual_step = self.actual_step + 1
        self.previous_step_button['state'] = tk.NORMAL
        load_step(self, gs = self.actual_block_rounds[self.actual_round - 1].gs[self.actual_g])
    if self.actual_step == cons.n_step:
        self.next_step_button['state'] = tk.DISABLED

def load_vs(self):
    v_nums = [[(x + (4*y)) for x in range(0, 4)] for y in range(0, 4)]
    total_rows = 4
    total_columns = 4
    self.entry_grid_vs = [[0 for x in range(total_rows)] for y in range(total_columns)]
    self.entry_grid_vs_ttp = [[0 for x in range(total_rows)] for y in range(total_columns)]
    for i in range(total_rows):
            for j in range(total_columns):
                self.e = tk.Entry(self.vs_frame, justify=tk.CENTER, width=5, font=('Arial',11,'bold'))
                self.e_ttp = ttp.ToolTip(self.e, self.v[4*i+j])
                
                self.e.grid(row=i+1, column=j+1)
                self.e.insert(tk.END, "v" + str(v_nums[i][j]))
                self.entry_grid_vs[j][i] = self.e
                self.entry_grid_vs_ttp[j][i] = self.e_ttp
                self.e.config( state="readonly")
    self.vs_frame.pack()
    for x in range(4):
        self.entry_grid_vs[x][0].config(fg="red")
    