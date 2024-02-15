import customtkinter as ctk
from settings import *
from tkinter import filedialog

class Panel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color = Dark_Grey)
        self.pack(fill = 'x', pady = 4, ipady = 8)

class Slider(Panel):
    def __init__(self, parent, text, var, min_value, max_value):
        super().__init__(parent= parent)

        self.rowconfigure((0,1), weight= 1)
        self.columnconfigure((0,1), weight= 1)

        ctk.CTkLabel(self, text = text).grid(row = 0, column = 0, sticky = 'w', padx = 5)
        self.num_label = ctk.CTkLabel(self, text= var.get() )
        self.num_label.grid(row = 0, column = 1, sticky = 'e', padx = 5)

        ctk.CTkSlider(self, orientation= 'horizontal', variable= var, fg_color= Slider_BG, from_= min_value, to = max_value, command= self.update_text).grid(row = 1, column = 0, columnspan = 2, sticky = 'nesw')

    def update_text(self, value):
        self.num_label.configure(text = f'{round(value, 2)}')

class SegmentPanel(Panel):
    def __init__(self,parent, text, var, options):
        super().__init__(parent = parent)

        ctk.CTkLabel(self, text = text).pack()
        ctk.CTkSegmentedButton(self,variable= var, values = options).pack(expand = True, fill = 'both', padx = 4, pady = 4)

class Switch(Panel):
    def __init__(self, parent, *args):
        super().__init__(parent = parent)

        for var, text in args:
            switch = ctk.CTkSwitch(self, text = text, variable = var, button_color= Blue, fg_color= Slider_BG)
            switch.pack(side = 'left', expand = True, fill = 'both', padx = 5, pady = 5)

class DropDown(ctk.CTkOptionMenu):
    def __init__(self, parent, var, options):
        super().__init__(parent, values= options, fg_color= Dark_Grey, button_color = DropDown_Main, button_hover_color = DropDown_Hover, dropdown_fg_color = DropDown_Menu, variable= var)
        self.pack(fill = 'x', pady = 4)

class File(Panel):
    def __init__(self, parent, name_string, file_string):
        super().__init__(parent)

        self.name_string = name_string
        self.name_string.trace('w', self.update_text)
        self.file_string = file_string

        ctk.CTkEntry(self, textvariable = self.name_string).pack(fill = 'x', padx = 20, pady = 20)
        frame = ctk.CTkFrame(self, fg_color= 'transparent')
        jpg_check = ctk.CTkCheckBox(frame, text= 'jpg', variable= self.file_string, command = lambda:self.click('jpg'), onvalue = 'jpg', offvalue= 'png')
        jpg_check.pack(side = 'left', fill = 'x', expand = True)

        png_check = ctk.CTkCheckBox(frame, text= 'png', variable= self.file_string, command = lambda:self.click('png'), onvalue = 'png', offvalue= 'jpg')
        png_check.pack(side = 'left', fill = 'x', expand = True)
        frame.pack(expand = True, fill = 'x', padx = 20)

        self.output = ctk.CTkLabel(self, text= ' ')
        self.output.pack()
    
    def click(self, value):
        self.file_string.set(value)
        self.update_text()

    def update_text(self, *args):
        if self.name_string.get():
            text = self.name_string.get().replace(' ','_') + '.' + self.file_string.get()
            self.output.configure(text = text)

class FilePath(Panel):
    def __init__(self, parent, path_string):
        super().__init__(parent)

        self.path_string = path_string
        
        ctk.CTkButton(self, text = 'Open', command= self.save).pack(pady = 5)
        ctk.CTkEntry(self, textvariable = self.path_string).pack(expand = True, fill = 'both', padx = 5, pady = 5)


    def save(self):
        self.path_string.set(filedialog.askdirectory())

class SaveButton(ctk.CTkButton):
    def __init__(self, parent, export_image, name_string, file_string, path_string):
        super().__init__(master = parent, text = 'save', command= self.save)
        self.pack(side = 'bottom', pady = 10)

        self.export_image = export_image
        self.name_string = name_string 
        self.file_string = file_string
        self.path_string = path_string

    def save(self):
        self.export_image(self.name_string.get(),self.file_string.get(),self.path_string.get())