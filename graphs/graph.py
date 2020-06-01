'''
Created on 7 Mar 2020

@author: julianporter
'''

from itertools import chain
from .graphic import Graphic, Stick
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
  
    def fixSize(self,w,h):
        if w!=self.width:
            self.width=w
            self.xs=list(range(0,self.width))
        self.height=h
        self.buildGUI()
    
    def __len__(self):
        return len(self.points)
        
    def add(self,y): 
        y=(1.0-self.range(y))*self.height
        self.ys=(self.ys+[y])[-self.width:]
        points=list(chain(*zip(self.xs,self.ys)))
        if len(points)>=4:
            self.graph.coords(self.line,points)
   
    def buildGUI(self):
        super().buildGUI()
        self.makeGrid(orientation=tk.HORIZONTAL)
         
    def clear(self):
        self.ys=[]
        self.graph.coords(self.line,self.basePoints)
        

class VUMeter(Graphic):
    
    def __init__(self,root,bounds=Range(-1,1),theme=DefaultTheme):
        super().__init__(root,bounds,theme)
        self.gradient=theme.gradient
        self.photo=tk.PhotoImage(width=self.width,height=self.height)
        self.graph.create_image(0,0,anchor=tk.NW,image=self.photo,state='normal')  
        self.graph.config(scrollregion=self.graph.bbox(0,0,self.width,self.height))
        self.rect=self.graph.create_rectangle(0,0,self.width,self.height,fill=self.theme.background)
    
        
    def buildGUI(self):
        super().buildGUI()
        
        cols = [str(self.gradient(1-(y/self.height))) for y in range(self.height)]
        xOffset = max(2,self.width//4)
        xRange = range(xOffset,self.width-xOffset)
        self.photo.blank()
        for x in xRange:
            self.photo.put(cols,(x,0))
            
        self.graph.coords(self.rect,0,0,self.width-1,self.height-1)
        self.graph.config(scrollregion=self.graph.bbox(0,0,self.width,self.height))
        
        self.makeGrid(orientation=tk.HORIZONTAL)
        
    def configure(self,**kwargs):
        super().configure(**kwargs)
        self.photo.configure(**kwargs)
            
    def bind(self,binding,callback):
        self.graph.bind(binding,callback)
        
    def grid(self,**kwargs):
        self.graph.grid(**kwargs)
  
    def fixSize(self,w,h):
        self.width=w
        self.height=h
        self.buildGUI()
               
    def add(self,y):
        y=(1.0-self.range(y))*self.height
        self.graph.coords(self.rect,0,0,self.width-1,y)

        
        
    def clear(self):
        self.graph.coords(self.rect,0,0,self.width-1,self.height-1)
        