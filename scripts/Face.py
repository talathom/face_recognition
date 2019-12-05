# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 23:24:15 2019

@author: thomas
"""

class Face:
    def calculate_midpoint(self):
        self.xmid = int((self.x + (self.x+self.w))/2)
        self.ymid = int((self.y + (self.y+self.h))/2)
        
    def __init__(self, x, y, w, h, z, name):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.z = z
        self.name = name
        self.calculate_midpoint()