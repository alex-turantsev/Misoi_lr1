#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
from collections import namedtuple
from math import sqrt
import random

Cluster = namedtuple('Cluster', ('points', 'center', 'n'))

def calculate_center(points):
    vals = [0,0]
    if len(points) < 1:
        return vals
    plen = 0
    for p in points:
        plen += 1
        vals[0] += p[0]
        vals[1] += p[1]
    return (vals[0]/plen, vals[1]/plen)

def calculate_distance(p1,p2):
    return sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

def kmeans(points, k=2, min_diff=1):
    if len(points) < 2:
        print "Not enough points for k-means"
        return
    centers = [points[0],points[1]]
    plists = []
    while 1:
        plists = [[] for i in range(k)]
        for p in points:
            smallest_distance = float('Inf')
            for i in range(k):
                distance = calculate_distance(p, centers[i])
                if distance < smallest_distance:
                    smallest_distance = distance
                    idx = i
            plists[idx].append(p)
        diff = 0
        for i in range(k):
            old = centers[i]
            new = calculate_center(plists[i])
            centers[i] = new
            diff = max(diff, calculate_distance(old, new))

        if diff < min_diff:
            break

    return plists
