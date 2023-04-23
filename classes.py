import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *

class scroll_frame(tk.Frame):
    def __init__(self, parent, bg, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)

        vscrollbar = ttk.Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = tk.Canvas(self, highlightthickness=0,
                           yscrollcommand=vscrollbar.set, bg=bg)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        self.interior = interior = tk.Frame(canvas,bg=bg)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        def _configure_interior(event):
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)


class classic_button(tk.Button):
    def __init__(self, master, text, command):
        tk.Button.__init__(self, master=master,text=text,command=command,
                           fg='#fff',bg='#42aaff',cursor='hand2',
                           relief='flat')
        self.anim = None
        self.bind('<Enter>', self.hover)
        self.bind('<Leave>', self.hover_off)

    def rgb(self, r, g, b):
        return '#%02x%02x%02x' % (r, g, b)
    
    def hover(self, event):
        self.anim = 'white'
        self.r = 66
        self.g = 170
        self.b = 255
        self.fr = 255
        self.fg = 255
        self.fb = 255
        self.white_color()
        self.blue_font_color()
        
    def hover_off(self, event):
        self.anim = 'blue'
        self.r = 255
        self.g = 255
        self.b = 255
        self.fr = 66
        self.fg = 170
        self.fb = 255
        self.blue_color()
        self.white_font_color()
        
    def white_color(self):
        if self.r == 255 and self.g == 255 and self.b == 255 or self.anim == 'blue':
            return
        if self.r < 255:
            self.r += 1
        if self.g < 255:
            self.g += 1
        if self.b < 255:
            self.b += 1
        self['bg'] = self.rgb(self.r, self.g, self.b)
        self.after(1, self.white_color)
        
    def blue_color(self):
        #print(self.r, self.g, self.b)
        if self.r == 66 and self.g == 170 and self.b == 255 or self.anim == 'white':
            return
        if self.r > 66:
            self.r -= 1
        if self.g > 170:
            self.g -= 1
        if self.b > 255:
            self.b -= 1
        self['bg'] = self.rgb(self.r, self.g, self.b)
        self.after(1, self.blue_color)

    def white_font_color(self):
        if self.fr == 255 and self.fg == 255 and self.fb == 255 or self.anim == 'white':
            return
        if self.fr < 255:
            self.fr += 1
        if self.fg < 255:
            self.fg += 1
        if self.fb < 255:
            self.fb += 1
        self['fg'] = self.rgb(self.fr, self.fg, self.fb)
        self.after(1, self.white_font_color)
        
    def blue_font_color(self):
        if self.fr == 66 and self.fg == 170 and self.fb == 255 or self.anim == 'blue':
            return
        if self.fr > 66:
            self.fr -= 1
        if self.fg > 170:
            self.fg -= 1
        if self.fb > 255:
            self.fb -= 1
        self['fg'] = self.rgb(self.fr, self.fg, self.fb)
        self.after(1, self.blue_font_color)

