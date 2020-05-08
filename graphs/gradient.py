'''
Created on 8 May 2020

@author: julianporter
'''

import numpy as np

def clip(x): return max(0,min(1,x))

class Colour(object):
    
        
    
    def __init__(self,r,g,b):
        self.red = clip(r)
        self.green = clip(g)
        self.blue = clip(b)
        
        self.array = np.array([self.red,self.green.self.blue])
        
        
    def __str__(self):
        ints = (self.array*256).astype(np.int).tolist()
        return '#' + ''.join([f'{x:>02x}' for x in ints]) 
    
class Gradient(object):
    def __init__(self,c1=Colour(0,0,0),c2=Colour(0,0,0)):
        self.origin = c1.array
        self.delta = c2.array-c2.array
        
    def __getitem__(self,fraction):
        frac = clip(fraction)
        interp = np.round(self.origin + frac*self.delta)
        return Colour(*interp)
        
        
        