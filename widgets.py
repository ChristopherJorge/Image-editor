from tkinter import filedialog as fd, messagebox, Canvas
from PIL import UnidentifiedImageError
import customtkinter as ctk
from settings import *
from widget_options import * 

class Import(ctk.CTkFrame):
    def __init__(self, parent, get_image):
        super().__init__(parent)
        self.grid(column = 0, columnspan = 2, row = 0, sticky = 'nesw')
        self.get_image = get_image

        ctk.CTkButton(self, text='Open Image', command=self.open).pack(expand = True)

    def open(self):
        try:
            path = fd.askopenfilename()
            self.get_image(path)
        except UnidentifiedImageError as e:
            messagebox.showerror('Error', message= f'{e}. Please try again')

class Display(Canvas):
    def __init__(self, parent, resize_img):
        super().__init__(parent, bd = 0, highlightthickness= 0, relief= 'ridge', background = BackGround_Color)
        self.grid(row = 0, column= 1, sticky= 'nesw', padx = 10, pady= 10)
        self.bind('<Configure>', resize_img)

class Close(ctk.CTkButton):
    def __init__(self, parent,close):
        self.close = close
        super().__init__(parent, text = 'X',fg_color= 'transparent', text_color= White, width = 40, height = 40, corner_radius= 0, hover_color = Close_Red, command= close)
        self.place(relx = 0.99, rely = 0.01, anchor = 'ne')

class Menu(ctk.CTkTabview):
    def __init__(self, parent, pos_vars, color_vars, effect_vars, export_image):
        super().__init__(parent)
        self.grid(row = 0, column = 0, sticky = 'nesw', pady = 10, padx = 10)

        # tabs 
        self.add('Position')
        self.add('Enhance')
        self.add('Color')
        self.add('Export')

        # Widgets 
        PositionFrame(self.tab('Position'), pos_vars)
        ColorFrame(self.tab('Color'), color_vars)
        EffectFrame(self.tab('Enhance'), effect_vars)
        Export(self.tab('Export'), export_image)

        


class PositionFrame(ctk.CTkFrame):
    def __init__(self, parent, pos_vars):
        super().__init__(parent, fg_color = 'transparent')
        self.pack(expand = True, fill = 'both')

        Slider(self, 'Rotation', pos_vars['rotate'], 0, 360)
        Slider(self, 'Zoom', pos_vars['zoom'], 0, 300)
        SegmentPanel(self, 'flip', pos_vars['flip'], Flip_options)

class ColorFrame(ctk.CTkFrame):
    def __init__(self, parent, color_vars):
        super().__init__(parent)
        self.pack(expand = True, fill = 'both')
        Switch(self,(color_vars['gray_scale'], 'Gray Scale'))
        Slider(self, 'Palette', color_vars['pallete'],1, 256)


class EffectFrame(ctk.CTkFrame):
    def __init__(self, parent, effect_vars):
        super().__init__(parent)
        self.pack(expand = True, fill = 'both')

        Slider(self, 'Brightness', effect_vars['brightness'], 0, 5)
        Slider(self, 'Blur', effect_vars['blur'], 0, 5)
        Slider(self, 'Vibrance', effect_vars['vibrance'], 0, 5)
        Slider(self, 'Sharpness', effect_vars['sharpness'], 1 , 5)
        Slider(self, 'Contrast', effect_vars['contrast'], 1 , 5)
        DropDown(self, effect_vars['effect'], Effect_Options)

class Export(ctk.CTkFrame):
      def __init__(self, parent, export_image):
        super().__init__(parent, fg_color = 'transparent')
        self.pack(expand = True, fill = 'both')

        self.name = ctk.StringVar()
        self.file = ctk.StringVar(value = 'jpg')
        self.path = ctk.StringVar()
        File(self, self.name, self.file)
        FilePath(self, self.path)
        SaveButton(self, export_image, self.name, self.file, self.path)