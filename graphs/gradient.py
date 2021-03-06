'''
Created on 8 May 2020

@author: julianporter
'''

import numpy as np


class CMeta(type):
    def __new__(cls,name,bases,attrs):
        c=super().__new__(cls,name,bases,attrs)
        c.Black = c(0,0,0)
        c.White = c(1,1,1)
        c.Red = c(1,0,0)
        c.Green = c(0,1,0)
        c.Blue = c(0,0,1)
        c.Yellow = c(1,1,0)
        c.Orange = c(1,0.5,0)
        return c
        
class Colour(metaclass=CMeta):
    
    def __init__(self,r,g,b):
        self.red = np.clip(r,0,1)
        self.green = np.clip(g,0,1)
        self.blue = np.clip(b,0,1)
        
        self.array = np.array([self.red,self.green,self.blue])
          
    def __str__(self):
        ints = (self.array*255.5).astype(np.int).tolist()
        return '#' + ''.join([f'{x:>02x}' for x in ints]) 
    
    def __repr__(self):
        return f'{self.array}'
    
    def __add__(self,other):
        return Colour(self.red+other.red,self.green+other.green,self.blue+other.blue)
    
    def __sub__(self,other):
        return Colour(self.red-other.red,self.green-other.green,self.blue-other.blue)
    
    def __mul__(self,other):
        if type(other) == Colour:
            return Colour(self.red*other.red,self.green*other.green,self.blue*other.blue)
        else:
            return Colour(other*self.red,other*self.green,other*self.blue)
        
    def __rmul__(self,other):
        return self.__mul__(other)
    
    def __invert__(self):
        return Colour(1-self.red,1-self.green,1-self.blue)
   
class Stop(object):
    
    def __init__(self,colour=Colour.Black,offset=0.0):
        self.colour=colour
        self.offset=offset
        
    def copy(self,offset=None):
        o = self.offset if offset is None else offset
        return Stop(colour=self.colour,offset=o)
    
    @property
    def array(self):
        return self.colour.array
        
    def __repr__(self):
        return f'{self.array} at offset {self.offset}'
      
class Gradient(object):
    def __init__(self,*stops):
        self.stops = sorted(stops,key = lambda s : s.offset)
        if len(self.stops)==0:
            self.stops=[Stop(Colour.Black,offset=0),Stop(Colour.White,offset=1)]
        self.first = self.stops[0]
        self.last = self.stops[-1]
        
        self.min = self.first.offset
        self.max = self.last.offset 
        
    def _find(self,v):
        for idx,stop in enumerate(self.stops):
            if v<stop.offset:
                return idx
        return len(self.stops)-1
        
    def __call__(self,value):
        v=np.clip(value,0,1)
        if v <= self.min: return self.first.colour
        elif v>= self.max: return self.last.colour
        else:
            index = self._find(v)
            before = self.stops[index-1]
            after = self.stops[index]
            delta=(v-before.offset)/(after.offset-before.offset)
            return before.colour + delta*(after.colour-before.colour)
    
    
          

        
        