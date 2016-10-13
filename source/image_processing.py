#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import numpy

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

    @staticmethod
    def area_selection(image):
        color = ((255,0,0),(0,255,0),(0,0,255),(255,255,0))
        image_copy = image.copy()
        pixels = image_copy.load()
        width, height = image.size
        areas = numpy.zeros((width, height)).astype(int)
        n = 0
        #print_pixles(pixels, width, height)
        for i in range(width):
            for j in range(height):
                if get_binary_pixel(pixels[i,j]) == 0:
                    if areas[max(0,i-1),j] == 0 and areas[i,max(0,j-1)] == 0:
                        n += 1
                        areas[i,j] = n
                        pixels[i,j] = color[n % len(color)]
                    else:
                        if areas[max(0,i-1),j] != 0:
                            areas[i,j] = areas[max(0,i-1),j]
                            #print i,j,areas[max(0,i-1),j],"i-1"
                        if areas[i,max(0,j-1)] != 0:
                            areas[i,j] = areas[i,max(0,j-1)]
                            #print i,j,areas[i,max(0,j-1)],"j-1"
                        pixels[i,j] = color[areas[i,j] % len(color)]
         #print n
        return image_copy

def get_binary_pixel(pixel):
    R,G,B = pixel
    binary = int((R+G+B)/3.0)
    return 1 if binary > 3 else 0

def print_pixles(pixels, width, height):
    print "pixels"
    for i in range(width):
        ar = []
        for j in range(height):
            ar.append(get_binary_pixel(pixels[i,j]))
        print ar
