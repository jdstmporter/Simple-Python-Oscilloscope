'''
Created on 7 May 2020

@author: julianporter
'''
import tkinter as tk
from util import Size

class Stick(object):
    
    ALL = (tk.N,tk.S,tk.E,tk.W)

class Graphic(object):
     
    def __init__(self,root,bounds,theme): 
        self.root=root
        self.range=bounds
        self.width=0
        self.height=0
        self.theme=theme
 
        self.graph=tk.Canvas(root,background=theme.background)
        self.graph.config(scrollregion=self.graph.bbox(tk.ALL))         
        self.graph.bind('<Configure>',lambda event : self.fixSize(event.width,event.height))
        
        self.ys=[]
        self.xs=[]
        self.axes=[]
        
        self.buildGUI()
        
    @property
    def size(self):
        return Size(int(self.graph['width']),int(self.graph['height']))
    
 
    
    def fixSize(self,w,h):
        pass
    
    def buildGUI(self):
        for item in self.axes:
            self.graph.delete(item)
        self.axes=[]   
    
    
    
    
     
    def bind(self,binding,callback):
        self.graph.bind(binding,callback)
    
    def configure(self,**kwargs):
        self.graph.configure(**kwargs)
        
    def pack(self,**kwargs):
        self.graph.pack(**kwargs)
        
    def grid(self,**kwargs):
        self.graph.grid(**kwargs) 
        
    def __call__(self,xformed):
        pass  

