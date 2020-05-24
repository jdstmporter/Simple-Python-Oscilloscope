'''
Created on 21 May 2020

@author: julianporter
'''

class Range(object):
    
    def __init__(self,mi,ma):
        self.min=mi
        self.max=ma
        
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
