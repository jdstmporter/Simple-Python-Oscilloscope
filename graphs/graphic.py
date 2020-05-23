'''
Created on 7 May 2020

@author: julianporter
'''
import tkinter as tk
from util import Size



class Graphic(object):
     
    def __init__(self,root,bounds,theme): 
        self.root=root
        self.range=bounds
        self.width=0
        self.height=0
        self.graph=tk.Canvas(root,background=theme.background)
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
        
    def pack(self,**kwargs):
        self.graph.pack(**kwargs)
        
    def grid(self,**kwargs):
        self.graph.grid(**kwargs) 
        
    def __call__(self,xformed):
        pass  

