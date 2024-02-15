# Importing necessary Libraries
import customtkinter as ctk
from PIL import Image, ImageTk, ImageOps, ImageEnhance, ImageFilter
from widgets import *

class App(ctk.CTk):
    def __init__(self, title, size):

        # Setting up the window
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        ctk.set_appearance_mode('dark')
        self.minsize(800, 500)
        self.paramaters()

        # Layout
        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 2, uniform = 'a')
        self.columnconfigure(1, weight= 6, uniform = 'a')

        # Canvas
        self.image_width = 0
        self.image_height = 0
        self.canvas_width = 0 
        self.canvas_height = 0

        # Widgets 
        self.Image_Import = Import(self, self.get_image)

        # running the window
        self.mainloop()

    def paramaters(self):
        self.pos_vars = {
            'rotate':  ctk.DoubleVar(value= Rotate_default),
            'zoom' : ctk.DoubleVar(value= zoom_default),
            'flip' : ctk.StringVar(value= Flip_options[0])

        }

        self.color_vars = {
            'gray_scale': ctk.BooleanVar(value = GrayScale_Default),
            'pallete': ctk.IntVar(value = Pallete_Default)
        }

        self.effect_vars = {
            'brightness': ctk.DoubleVar(value = Brightness_Default),
            'blur': ctk.DoubleVar(value = Blur_Default),
            'contrast': ctk.IntVar(value= Contrast_Default),
            'vibrance': ctk.DoubleVar(value = Vibrance_Default),
            'sharpness': ctk.DoubleVar(value = Sharpness_Default),
            'effect': ctk.StringVar(value = Effect_Options[0])
        }

        for var in self.pos_vars.values():
            var.trace('w', self.manipulate_img)
        for var in self.effect_vars.values():
            var.trace('w', self.manipulate_img)
        for var in self.color_vars.values():
            var.trace('w', self.manipulate_img)

    def manipulate_img(self, *args):
        self.image = self.original
        
        # Position manipulation 
        self.image = self.image.rotate(self.pos_vars['rotate'].get())
        
        self.image = ImageOps.crop(image = self.image, border = self.pos_vars['zoom'].get())
        
        if self.pos_vars['flip'].get() == 'X':
            self.image = ImageOps.mirror(self.image)
        if self.pos_vars['flip'].get() == 'Y':
            self.image = ImageOps.flip(self.image)
        if self.pos_vars['flip'].get() == 'Both':
            self.image = ImageOps.mirror(self.image)
            self.image = ImageOps.flip(self.image)

        # Enhancement manipulation
        brightness_enhancer = ImageEnhance.Brightness(self.image)
        self.image = brightness_enhancer.enhance(self.effect_vars['brightness'].get())

        Vibrance_enhancer = ImageEnhance.Color(self.image)
        self.image = Vibrance_enhancer.enhance(self.effect_vars['vibrance'].get())

        Sharpness_enhancer = ImageEnhance.Sharpness(self.image)
        self.image = Sharpness_enhancer.enhance(self.effect_vars['sharpness'].get())

        Contrast_enhancer = ImageEnhance.Contrast(self.image)
        self.image = Contrast_enhancer.enhance(self.effect_vars['contrast'].get())

        self.image = self.image.filter(ImageFilter.GaussianBlur(self.effect_vars['blur'].get()))

        match self.effect_vars['effect'].get():
            case 'Contour': self.image = self.image.filter(ImageFilter.CONTOUR)
            case 'Detail': self.image = self.image.filter(ImageFilter.DETAIL)
            case 'EdgeEnhance': self.image = self.image.filter(ImageFilter.EDGE_ENHANCE)
            case 'Emboss': self.image = self.image.filter(ImageFilter.EMBOSS)
            case 'MaxFilter': self.image = self.image.filter(ImageFilter.MaxFilter)
            case 'MinFilter': self.image = self.image.filter(ImageFilter.MinFilter)
            case 'MedianFilter': self.image = self.image.filter(ImageFilter.MedianFilter)
            case 'ModeFilter': self.image = self.image.filter(ImageFilter.ModeFilter)
            case 'Smooth': self.image = self.image.filter(ImageFilter.SMOOTH)

        # Color manipulation
        self.image = self.image.convert('P', palette= Image.Palette.ADAPTIVE, colors= self.color_vars['pallete'].get())

        if self.color_vars['gray_scale'].get():
            self.image = ImageOps.grayscale(self.image)


        # Place the manipulated image
        self.place_img()

    def get_image(self, path):
            self.original = Image.open(path)
            self.image = self.original
            self.image_ratio = self.image.size[0] / self.image.size[1]
            self.image_tk = ImageTk.PhotoImage(self.image)

            self.Image_Import.grid_forget()

            self.output = Display(self, self.resize_img)
            self.close_button = Close(self, self.close)
            self.menu = Menu(self, self.pos_vars, self.color_vars, self.effect_vars, self.export_img)
    
    def close(self): 
        self.output.grid_forget()
        self.close_button.grid_forget()
        self.menu.grid_forget()

        self.Image_Import = Import(self, self.get_image)

    def resize_img(self, event):
        # Canvas Ratio 
        canvas_ratio = event.width / event.height 

        self.canvas_width = event.width
        self.canvas_height = event.height
        # resize
        if canvas_ratio > self.image_ratio: 
            self.image_height = int(event.height)
            self.image_width = int(self.image_height * self.image_ratio)
        else:
            self.image_width = int(event.width) 
            self.image_height = int(self.image_width / self.image_ratio)
        
        self.place_img()

    def place_img(self):
        self.output.delete('all')
        resized = self.image.resize((self.image_width, self.image_height))
        self.image_tk = ImageTk.PhotoImage(resized)
        self.output.create_image(self.canvas_width / 2, self.canvas_height / 2 ,image= self.image_tk)

    def export_img(self, name, file, path):
        export_string = f'{path}/{name}.{file}'
        self.image.save(export_string)
        messagebox.showinfo('Notice', 'Image Successfully Saved!')

App('Image Editor',(1000,600))

