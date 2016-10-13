#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import Tkinter as tk
import tkFileDialog
import os
import os.path
from PIL import ImageTk, Image
import subprocess
import platform
import ntpath
from image_processing import *

class ApplicationView:
    def __init__(self):
        pass

    def initialize(self,app):
        self.root = app
        self.histogram_window = None
        self.imageFrame = tk.Frame(app, bg="white")
        self.imageFrame.pack(side = "left", fill = "both", expand = "True")

        self.buttonsFrame = tk.Frame(app, width = 0)
        self.buttonsFrame.pack(side = "right",fill = "y")

        self.image_path = '/Users/alex/Downloads/unspecified2.jpeg'
        self.imageLabel = tk.Label(self.imageFrame)
        self.imageLabel.pack(fill = "both", expand = "True")
        self.image = None
        try:
            self.change_image(Image.open(self.image_path))
        except:
            pass
        self.create_left_buttons()

        self.file_opt = options = {}
        options['defaultextension'] = '.jpg'
        options['filetypes'] = [('image files', ('.jpeg','.jpg','.JPG','.JPEG','.png','.PNG'))]
        options['initialdir'] = os.path.expanduser('~')
        options['initialfile'] = 'myfile.jpg'
        options['parent'] = app.root
        options['title'] = 'Choose file'

    def create_left_buttons(self):
        buttons_width = 13

        self.create_button(parent=self.buttonsFrame,text="Load image",width=buttons_width,command=self.load_image_with_ask)
        self.create_button(parent=self.buttonsFrame,text="Make grayscale",width=buttons_width,command=lambda: self.image_process("grayscale"))
        binary_frame = tk.Frame(self.buttonsFrame)
        binary_frame.pack( side = "top", padx = 5, pady = 0)
        self.create_button(parent=binary_frame,text="Make binary",width=buttons_width,command=lambda: self.image_process("binary"),pady=1)
        b_label = tk.Label(binary_frame, text = "Treshhold", width = 7)
        b_label.pack(side = "left")
        self.binary_treshhold = tk.StringVar()
        b_field = tk.Entry(binary_frame, textvariable=self.binary_treshhold,width = 5)
        b_field.pack( side = "right",padx = 3)
        self.binary_treshhold.set(100)

        self.create_button(parent=self.buttonsFrame,text="Select areas",width=buttons_width,command=lambda: self.image_process("areas"),pady=1)

        self.create_button(parent=self.buttonsFrame,text="Reset",width=buttons_width,command=lambda: self.load_image())
        self.create_button(parent=self.buttonsFrame,text="Save image",width=buttons_width,command=lambda: self.save_image(),pady=6)

    def create_button(self, parent, text, width, command, pady=4):
        button = tk.Button(parent , text=text, width = width, command = command)
        button.pack( side = "top", padx = 5, pady = pady)

    def load_image_with_ask(self):
        ff = tkFileDialog.askopenfile(mode='r',**self.file_opt)
        if ff is not None:
            self.image_path = ff.name
            self.load_image()

    def load_image(self):
        file_extension = os.path.splitext(self.image_path)[1]
        image = Image.open(self.image_path)
        if file_extension == '.png':
            timage = Image.new("RGB", image.size, (255, 255, 255))
            timage.paste(image, mask=image.split()[3])
            image = timage
        self.change_image(image)

    def save_image(self):
        self.file_opt['initialfile'] = "1"+ntpath.basename(self.image_path);
        f = tkFileDialog.asksaveasfile(mode='w', **self.file_opt )
        if f is None:
            return
        self.image.save(f.name)

    def image_process(self,id):
        image = None
        if id == "binary":
            try:
                b = int(self.binary_treshhold.get())
                if  b < 0 or b > 255:
                    return
                image = image_processing.image_binary(self.imagecopy,b)
            except:
                pass
        if id == "grayscale":
            image = image_processing.grayscale(self.imagecopy)
        if id == "areas":
            image = image_processing.area_selection(self.imagecopy)
        if image != None:
            self.change_image(image)

    def change_image(self, new_image):
        self.image = new_image
        self.imagecopy = self.image.copy()
        self.update_label_image(self.image)

    def update_label_image(self, new_image):
        img = ImageTk.PhotoImage(new_image)
        self.imageLabel.configure(image = img)
        self.imageLabel.image = img
