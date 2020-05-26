'''
Created on 7 May 2020

@author: julianporter
'''
import tkinter as tk
from util import Size

class Stick(object):
    
    ALL = (tk.N,tk.S,tk.E,tk.W)

class Graphic(object):
     
    def __init__(self,root,bounds,theme,scrollable=False,width=0,height=0,sxFactor=1,syFactor=1): 
        self.root=root
        self.range=bounds
        self.width=width
        self.height=height
        self.swidth=int(width*sxFactor)
        self.sheight=int(height*syFactor)
        self.sxFactor=sxFactor
        self.syFactor=syFactor
        
        self.xscroll=None
        self.yScroll=None
        
        if scrollable:
            self.graph=tk.Canvas(root,background=theme.background,width=width,height=height)
            self.graph.config(width=width,height=height)
            self.graph.config(scrollregion=(0,0,self.swidth,self.sheight))
            if self.sxFactor>1:
                self.xscroll=tk.Scrollbar(self.root,orient=tk.HORIZONTAL)
                self.xscroll.config(command=self.graph.xview)
                self.graph.config(xscrollcommand=self.xscroll.set)
            if self.syFactor>1:
                self.yscroll=tk.Scrollbar(self.root,orient=tk.VERTICAL)
                self.yscroll.config(command=self.graph.yview)
                self.graph.config(yscrollcommand=self.yscroll.set)
        else:                
            self.graph=tk.Canvas(root,background=theme.background)
            self.graph.config(scrollregion=self.graph.bbox(tk.ALL))
        self.graph.bind('<Configure>',lambda event : self.fixSize(event.width,event.height))
        
        self.ys=[]
        self.xs=[]
        
    @property
    def size(self):
        return Size(int(self.graph['width']),int(self.graph['height']))
    
    def fixSize(self,w,h):
        pass
    
     
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

