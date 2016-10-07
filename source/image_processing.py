#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

class image_processing():
    @staticmethod
    def image_binary(image,threshold):
        image_copy = image.copy()
        pixels = image_copy.load()
        width, height = image.size
        for i in range(width):
            for j in range(height):
                R,G,B = pixels[i,j]
                gray = int((R+G+B)/3)
                gray = 0 if gray <=threshold else 255
                pixels[i,j] = (gray, gray, gray)
        return image_copy

    @staticmethod
    def grayscale(image):
        image_copy = image.copy()
        pixels = image_copy.load()
        width, height = image.size
        for i in range(width):
            for j in range(height):
                R,G,B = pixels[i,j]
                gray = int(0.3*R + 0.59*G + 0.11*B)
                pixels[i,j] = (gray, gray, gray)
        return image_copy
