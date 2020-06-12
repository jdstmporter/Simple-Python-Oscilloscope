'''
Created on 7 Mar 2020

@author: julianporter
'''

from itertools import chain
from ..graphic import Graphic
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
        self.clear()
        super().buildGUI()
        self.makeGrid(orientation=tk.HORIZONTAL)
         
    def clear(self):
        self.ys=[]
        self.graph.coords(self.line,self.basePoints)
        
  
        

        