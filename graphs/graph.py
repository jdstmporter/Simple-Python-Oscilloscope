'''
Created on 7 Mar 2020

@author: julianporter
'''

import tkinter as tk
from itertools import chain


class Range(object):
    
    def __init__(self,mi,ma):
        self.min=mi
        self.max=ma
        
    def __len__(self):
        return self.max-self.min
    
    def __call__(self,value):
        return (value-self.min)/(self.max-self.min)
    
class Size(object):
    
    def __init__(self,width,height):
        self.width=width
        self.height=height
        
    def scaleY(self,y):
        return y*self.height
        
        
        
class Graph(object):
    
    def __init__(self,root,bounds=Range(-1,1),
                 xscale=1,background='black',line='red'):
        self.root=root
        self.range=bounds
        self.xscale=xscale
        self.width=0
        self.height=0
        self.graph=tk.Canvas(root,background=background)
        self.graph.grid(column=0, row=0, sticky=(tk.N,tk.S,tk.E,tk.W))
        self.graph.config(scrollregion=self.graph.bbox(tk.ALL))
        #self.graph.pack()
        #self.graph.bind('<Configure>',self.onResize)
        
        self.size = Size(0,0)
        self.basePoints=[-1,self.height,-1,self.height]
        self.line = self.graph.create_line(*self.basePoints,fill=line)
        
        self.ys=[]
        self.xs=[]
        
        
    def bind(self,binding,callback):
        self.graph.bind(binding,callback)
    
    
        
    def grid(self,**kwargs):
        self.graph.grid(**kwargs)
  
    def pack(self):
        s=Size(int(self.graph['width']),int(self.graph['height']))
        if s.width!=self.width:
            self.width=s.width
            self.xs=list(range(0,self.width))
        self.height=s.height
    
    @property
    def N(self):
        return len(self.points)
        
    def add(self,y):
        self.pack()
        
        #x=self.xscale*self.N/2
        y=(1.0-self.range(y))*self.height
        self.ys=(self.ys+[y])[-self.width:]
        points=list(chain(*zip(self.xs,self.ys)))
        print(f'{y}')
        #self.points+=[x,y]
        #if self.N>2*self.width:
        #    self.points=self.points[2:]
        #    for i in range(0,self.N,2): self.points[i]-=self.xscale
        if len(self.ys)>=2:
            self.graph.coords(self.line,points)
        
        
        
    def clear(self):
        #self.points=[0,self.height,0,self.height]
        self.ys=[]
        self.graph.coords(self.line,self.basePoints)
        
    
          
        