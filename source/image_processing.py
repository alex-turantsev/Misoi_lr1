#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
from image_areas import *

class image_processing(object):
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
        areas = image_areas(width=width,height=height)
        n = 0
        #print_pixles(pixels, width, height)
        for i in range(width):
            for j in range(height):
                if get_binary_pixel(pixels[i,j]) == 0:
                    up, left = areas.get_up_and_left(i,j)
                    if up == 0 and left == 0:
                        n += 1
                        areas.add_new_area()
                        areas.add_pixel_to_area(n-1,i,j)
                        pixels[i,j] = color[n % len(color)]
                    else:
                        if left != 0 and up == 0:
                            areas.add_pixel_to_area(left,i,j)
                        elif left == 0 and up != 0:
                            areas.add_pixel_to_area(up,i,j)
                        elif left != up:
                            areas.add_pixel_to_area(up,i,j)
                            areas.merge_areas(up, left)
                        else:
                            areas.add_pixel_to_area(up,i,j)
        #print areas
        for i in range(width):
            for j in range(height):
                area = areas.get_area_on_pixel(i,j)
                if area != 0:
                    pixels[i,j] = color[area % len(color)]

        areas.print_areas_number()
        areas.compute_attrubutes()

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
