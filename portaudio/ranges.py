'''
Created on 14 May 2020

@author: julianporter
'''

import numpy as np

class Range(object):
    
    
    
    
    def __init__(self,mi=-1,ma=1):
        self.min=mi
        self.max=ma
        self.scale = 1.0/(ma-mi)
        
    def __len__(self):
        return self.max-self.min
    
    def __contains__(self,v):
        return self.min <=v and v <= self.max
    
    def clip(self,x):
        return np.clip(x,self.min,self.max)
    
    def __call__(self,value):
        return (self.clip(value)-self.min)*self.scale
    
    def __repr__(self):
        return f'[{self.min},{self.max}]'