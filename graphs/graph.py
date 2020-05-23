'''
Created on 7 Mar 2020

@author: julianporter
'''

from itertools import chain
from .graphic import Graphic
from util import Range, DefaultTheme
import tkinter as tk


        
        
class Graph(Graphic):
    
    def __init__(self,root,bounds=Range(-1,1),theme=DefaultTheme):
        super().__init__(root,bounds,theme)
        self.basePoints=[-1,self.height,-1,self.height]
        self.line = self.graph.create_line(*self.basePoints,**theme.data)
       
    def bind(self,binding,callback):
        self.graph.bind(binding,callback)
        
    def grid(self,**kwargs):
        self.graph.grid(**kwargs)
  
    def fixSize(self):
        s=self.size
        if s.width!=self.width:
            self.width=s.width
            self.xs=list(range(0,self.width))
        self.height=s.height
    
    def __len__(self):
        return len(self.points)
        
    def add(self,y):
        self.fixSize()
        
        y=(1.0-self.range(y))*self.height
        self.ys=(self.ys+[y])[-self.width:]
        points=list(chain(*zip(self.xs,self.ys)))
        if len(self.ys)>=2:
            self.graph.coords(self.line,points)
        
        
        
    def clear(self):
        self.ys=[]
        self.graph.coords(self.line,self.basePoints)
        

class VUMeter(Graphic):
    
    def __init__(self,root,bounds=Range(-1,1),theme=DefaultTheme):
        super().__init__(root,bounds,theme)
        self.photo=tk.PhotoImage(width=self.width,height=self.height)
        self.graph.create_image(0,0,anchor=tk.NW,image=self.photo,state='normal')
        points=[0,0,self.width,self.height]
        self.rect=self.graph.create_rectangle(*points,fill=theme.background)
        self.gradient=theme.gradient
        self.graph.config(scrollregion=self.graph.bbox(tk.ALL))
        #self.photo.grid(column=0,row=0,sticky=(tk.N, tk.S, tk.E, tk.W))
        
        
        
    def redraw(self):
        
        cols =  [str(self.gradient(1-(y/self.height))) for y in range(self.height)]
        for x in range(self.width):
            self.photo.put(cols,(x,0))
             
        
        
    def bind(self,binding,callback):
        self.graph.bind(binding,callback)
        
    def grid(self,**kwargs):
        self.graph.grid(**kwargs)
  
    def fixSize(self):
        s=self.size
        self.width=s.width
        if s.height != self.height:
            self.height=s.height
            self.redraw()
            
        
    def add(self,y):
        self.fixSize()
        
        y=(1.0-self.range(y))*self.height
        self.graph.coords(self.rect,0,0,self.width-1,y)
        
        
    def clear(self):
        pass
        self.graph.coords(self.rect,0,0,self.width-1,self.height)
        