'''
Created on 7 May 2020

@author: julianporter
'''
import tkinter as tk
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

    
class Size(object):
    
    def __init__(self,width,height):
        self.width=width
        self.height=height
        
    def scaleY(self,y):
        return y*self.height
     

class Graphic(object):
     
    def __init__(self,root,bounds,xscale,background,line):
        self.root=root
        self.range=bounds
        self.xscale=xscale
        self.width=0
        self.height=0
        self.fill=line
        self.graph=tk.Canvas(root,background=background)
        self.graph.grid(column=0, row=0, sticky=(tk.N,tk.S,tk.E,tk.W))
        self.graph.config(scrollregion=self.graph.bbox(tk.ALL))
        
        #self.graph.bind('<Configure>',self.onResize)
        
        self.ys=[]
        self.xs=[]
        
    @property
    def size(self):
        return Size(int(self.graph['width']),int(self.graph['height']))
    
     
    def bind(self,binding,callback):
        self.graph.bind(binding,callback)
    
    def configure(self,**kwargs):
        self.graph.configure(**kwargs)
        
    def pack(self):
        self.graph.pack()
        
    def grid(self,**kwargs):
        self.graph.grid(**kwargs) 
        
    def __call__(self,xformed):
        pass  
