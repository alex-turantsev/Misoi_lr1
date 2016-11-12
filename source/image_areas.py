#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import numpy
import math
from kmeans import kmeans

class image_areas(object):
    def __init__(self, width, height):
        self.size = width,height
        self.pixel_grid = numpy.zeros((width, height)).astype(int)
        self.areas_pixels = []
        self.areas_pixels.append([])
        self.areas_atributes = []

    def get_up_and_left(self, i, j):
        return self.pixel_grid[i,max(0,j-1)], self.pixel_grid[max(0,i-1),j]

    def add_new_area(self):
        self.areas_pixels.append([])

    def add_pixel_to_area(self, area, i, j):
        self.areas_pixels[area].append((i,j))
        self.pixel_grid[i,j] = area

    def merge_areas(self, area1, area2):
        areas = self.areas_pixels
        areas[area1].extend(areas[area2])
        for i1,j1 in areas[area2]:
            self.pixel_grid[i1,j1] = area1
        areas[area2] = []

    def get_area_on_pixel(self, i, j):
        return self.pixel_grid[i,j]

    def print_areas_number(self):
        count = 0
        for area in self.areas_pixels:
            if len(area) > 1:
                count += 1
        print count

    def compute_attrubutes(self):
        self.areas_atributes = []
        for area in self.areas_pixels:
            if len(area) > 1:
                self.areas_atributes.append(area_attribute(area,self.pixel_grid))

    def compute_clusters(self):
        points = [[attr.density, attr.elongation] for attr in self.areas_atributes]
        k = kmeans(points)
        clusters = []
        for i in range(len(k)):
            clusters.append([])
            for el in k[i]:
                clusters[i].append(points.index(el))
        return clusters

class area_attribute(object):
    pixels = []
    perimetr = 0
    square = 0
    elongation = 0
    main_axis_orientation = 0
    def __init__(self, area, grid):
        self.square = len(area)
        self.pixels = area
        min_x = 10000
        max_x = 0
        min_y = 10000
        max_y = 0
        xI = 0
        yI = 0
        m11 = 0
        m02 = 0
        m20 = 0
        for i,j in self.pixels:
            xI += i
            yI += j
            if self.is_border_pixel(i,j, grid):
                self.perimetr += 1
            if min_x > i:
                min_x = i
            if max_x < i:
                max_x = i
            if min_y > j:
                min_y = j
            if max_y < j:
                max_y = j
        self.mass_center = (xI/self.square, yI/self.square)
        self.density = (self.perimetr**2)/self.square

        for i,j in self.pixels:
            m20 = m20 + (i - self.mass_center[0])**2
            m02 = m02 + (j - self.mass_center[1])**2
            m11 = m11 + (i - self.mass_center[0]) * (j - self.mass_center[1])

        self.elongation = (m20 + m02 + math.sqrt((m20-m02)**2 + 4*m11*m11))/(m20 + m02 - math.sqrt((m20-m02)**2 + 4*m11**2))
        self.main_axis_orientation = 0.5*math.atan((2*m11)/(m20-m02))

    def __str__(self):
        return "p-{0} s-{1} mc-{2} de-{3} el-{4:.3f} ori-{5:.3f}".format(self.perimetr,self.square,self.mass_center,self.density,self.elongation,self.main_axis_orientation)

    __repr__ = __str__

    def is_border_pixel(self, i, j, gr):
        w, h = gr.shape
        return not gr[i,max(0,j-1)] or not gr[i,min(h,j+1)] or not gr[max(0,i-1),j] or not gr[min(w,i+1),j]
