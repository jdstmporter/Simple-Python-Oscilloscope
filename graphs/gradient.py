'''
Created on 8 May 2020

@author: julianporter
'''

import numpy as np


def clip(x): return max(0,min(1,x))

class Colour(object):
    
    def __init__(self,r,g,b,offset=0.0):
        self.red = clip(r)
        self.green = clip(g)
        self.blue = clip(b)
        self.offset = clip(offset)
        
        self.array = np.array([self.red,self.green,self.blue])
          
    def __str__(self):
        ints = (self.array*255.5).astype(np.int).tolist()
        return '#' + ''.join([f'{x:>02x}' for x in ints]) 
    
    def __repr__(self):
        return f'{self.array} at offset {self.offset}'
    
    def copy(self,offset=None):
        c=Colour(self.red,self.green,self.blue,offset=self.offset)
        if offset is not None:
            c.offset=clip(offset)
        return c
    

    
class Segment(object):
    def __init__(self,c1=Colour(0,0,0),c2=Colour(0,0,0)):
        self.origin = c1.array
        self.delta = c2.array-c1.array
        self.range = (c1.offset,c2.offset)
        self.scale = self.range[1]-self.range[0]
    
    def __contains__(self,v):
        return self.range[0] <=v and v <= self.range[1]
    
    def __call__(self,offset):
        o=clip(offset)
        frac = (o - self.range[0])/self.scale
        interp = self.origin + frac*self.delta
        return Colour(*interp,offset=o)
    
    def __repr__(self):
        return f'origin={self.origin} slope={self.delta} range={self.range}'

        
class Gradient(object):
    def __init__(self,*colours):
        s=colours[0]
        if s.offset>0 : colours.insert(0,s.copy(offset=0))
        e=colours[-1]
        if e.offset<1 : colours.append(e.copy(offset=1))
        
        segs=[]
        for idx in range(len(colours)-1):
            segs.append(Segment(colours[idx],colours[idx+1]))
        self.segments=segs
        
    def find(self,value):
        matched=[s for s in self.segments if value in s]
        if len(matched)==0: return None
        else: return matched[0]
        
    def __call__(self,value):
        v=clip(value)
        s=self.find(v)
        if s is None: return None
        return s(v)
    
    @classmethod
    def greyscale(cls):
        return Gradient(Colour(0,0,0,offset=0),Colour(1,1,1,offset=1))
          

        
        