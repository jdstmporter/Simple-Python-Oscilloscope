'''
Created on 8 May 2020

@author: julianporter
'''

import numpy as np


def clip(x): return max(0,min(1,x))

class CMeta(type):
    def __new__(cls,name,bases,attrs):
        c=super().__new__(cls,name,bases,attrs)
        c.Black = c(0,0,0)
        c.White = c(1,1,1)
        c.Red = c(1,0,0)
        c.Green = c(0,1,0)
        c.Blue = c(0.28,0.46,1)
        c.Indigo = c(0.29,0,0.5)
        c.Violet = c(0.33,0.1,0.54)
        c.Yellow = c(1,1,0)
        c.Orange = c(1,0.64,0)
        c.Gold = c(1,0.84,0)
        return c
        
class Colour(metaclass=CMeta):
    
    def __init__(self,r,g,b):
        self.red = clip(r)
        self.green = clip(g)
        self.blue = clip(b)
        
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
    def __init__(self,*stops,name='gradient'):
        self.name=name
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
        v=clip(value)
        if v <= self.min: return self.first.colour
        elif v>= self.max: return self.last.colour
        else:
            index = self._find(v)
            before = self.stops[index-1]
            after = self.stops[index]
            delta=(v-before.offset)/(after.offset-before.offset)
            return before.colour + delta*(after.colour-before.colour)
    
class Gradients(object):
    
    def __init__(self,std=0):
        self.default=std
        self.grads=[
            Gradient(Stop(Colour.Black, offset=0),
                     Stop(Colour.White, offset=1),
                     name='GreyScale'),
            Gradient(Stop(Colour.Blue, offset=0),
                     Stop(Colour.Green, offset=0.2),
                     Stop(Colour.Yellow, offset=0.5),
                     Stop(Colour.Orange, offset=0.7),
                     Stop(Colour.Red, offset=0.97),
                     name='RedGreenBlue'),
            Gradient(Stop(Colour.Violet, offset=0),
                     Stop(Colour.Indigo, offset=0.16),
                     Stop(Colour.Blue, offset=0.32),
                     Stop(Colour.Green, offset=0.48),
                     Stop(Colour.Yellow, offset=0.64),
                     Stop(Colour.Orange, offset=0.8),
                     Stop(Colour.Red, offset=0.96),
                     name='ROYGBIV'),
            Gradient(Stop(Colour.Black,offset=0),
                     Stop(Colour.Violet, offset=0.25),
                     Stop(Colour.Indigo, offset=0.5),
                     Stop(Colour.Red, offset=0.75),
                     Stop(Colour.Yellow, offset=0.96),
                     name='Audition'),
            Gradient(Stop(Colour.Black,offset=0),
                     Stop(Colour(0.1,0.1,0.1),offset=0.25),
                     Stop(Colour.Orange, offset=0.50),
                     Stop(Colour.Gold, offset=0.75),
                     Stop(Colour.Yellow, offset=0.96),
                     name='Yellowish')
        ]
        
        self.searchable = { g.name : g for g in self.grads }
    
    
    def __call__(self):
        return self.grads[self.default]    
    
    def __getitem__(self,key):
        try:
            if type(key)==str:
                return self.searchable[key]
            elif type(key)==int:
                return self.grads[key]
            else:
                raise Exception('No such gradient')
        except:
            return None
        
    def __getattr__(self,name):
        return self[name]
    
    def __iter__(self):
        return iter(self.grads)
    
    def __len__(self):
        return len(self.grads)
    
    def keys(self):
        return [g.name for g in self.grads]
    
    
        


        