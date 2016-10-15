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
        areas1 = []
        areas1.append([])
        n = 0
        #print_pixles(pixels, width, height)
        for i in range(width):
            for j in range(height):
                if get_binary_pixel(pixels[i,j]) == 0:
                    up = areas[i,max(0,j-1)]
                    left = areas[max(0,i-1),j]
                    if up == 0 and left == 0:
                        n += 1
                        areas1.append([])
                        areas1[n].append((i,j))
                        areas[i,j] = n
                        pixels[i,j] = color[n % len(color)]
                    else:
                        if left != 0 and up == 0:
                            areas[i,j] = left
                            areas1[left].append((i,j))
                            #print i,j,areas[max(0,i-1),j],"i-1"
                        elif left == 0 and up != 0:
                            areas[i,j] = up
                            areas1[up].append((i,j))
                            #print i,j,areas[i,max(0,j-1)],"j-1"
                        elif left != up:
                            #print left, up
                            areas1[up].extend(areas1[left])
                            areas[i,j] = up
                            areas1[up].append((i,j))
                            for i1,j1 in areas1[left]:
                                areas[i1,j1] = up
                            areas1[left] = []
                        else:
                            areas[i,j] = up
                            areas1[up].append((i,j))
        #print areas
        for i in range(width):
            for j in range(height):
                if areas[i,j] != 0:
                    pixels[i,j] = color[areas[i,j] % len(color)]
        count = 0
        for item in areas1:
            if len(item) > 1:
                count += 1
                print len(item)
        print count
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
