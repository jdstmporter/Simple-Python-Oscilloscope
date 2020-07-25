'''
Created on 21 May 2020

@author: julianporter
'''
import math

class Range(object):
    
    def __init__(self,mi,ma):
        self.min=mi
        self.max=ma
        
    def bounds(self):
        return (self.min,self.max)
        
    def closure(self,width=1):
        return Range(width*math.ceil(self.min/width),width*math.ceil(self.max/width))
    
    def int(self):
        return (int(self.min),int(self.max))
    
    def clip(self,other):
        return Range(max(self.min,other.min),min(self.max,other.max))
        
    def __len__(self):
        return self.max-self.min
    
    def __contains__(self,v):
        return self.min <=v and v <= self.max
    
    def __call__(self,value):
        return (value-self.min)/(self.max-self.min)
    
    def __repr__(self):
        return f'[{self.min},{self.max}]'
    
class Size(object):
    
    def __init__(self,width=0,height=0):
        self.width=width
        self.height=height
        
    def scaleY(self,y):
        return y*self.height
    
    def __eq__(self,other):
        return self.width==other.width and self.height==other.height
    
    def __ne__(self,other):
        return self.width != other.width or self.height != other.height
