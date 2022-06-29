import tkinter as tk

class ToolTip(object):

    def __init__(self, widget, text='widget info', width = None, height= None):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.width = width
        self.height = height
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def update_text(self, text = "Update"):
        self.text = text
        
    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20

        self.tw = tk.Toplevel(self.widget)
        
        self.tw.wm_attributes("-topmost", 1)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x , y))

        if self.height == None and self.width == None:

            label = tk.Label(self.tw, text=self.text, justify='left', font='Helvetica 11', background="#ffffff", relief='solid', borderwidth=1, wraplength = self.wraplength)
        else:
            label = tk.Label(self.tw, text=self.text, justify='left', font='Helvetica 11', background="#ffffff", relief='solid', borderwidth=1, width=self.width, height = self.height)
        
        label.pack(ipadx=1)

    def hidetip(self):

        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()