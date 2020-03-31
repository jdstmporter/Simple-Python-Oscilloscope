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
    
    def __init__(self,root,bounds=Range(-1,1),width=200,height=400,
                 xscale=1,background='black',line='red'):
        self.root=root
        self.range=bounds
        self.xscale=xscale
        self.width=width
        self.height=height
        self.graph=tk.Canvas(root,width=self.width,height=self.height,background=background)
        self.graph.grid(column=0, row=0, sticky=(tk.N,tk.S,tk.E,tk.W))
        self.graph.config(scrollregion=self.graph.bbox(tk.ALL))
        #self.graph.pack()
        #self.graph.bind('<Configure>',self.onResize)
        
        self.basePoints=[-1,self.height,-1,self.height]
        self.line = self.graph.create_line(*self.basePoints,fill=line)
        
        self.xs=list(range(0,self.width))
        self.ys=[]
        
    def grid(self,**kwargs):
        self.graph.grid(**kwargs)
  
    def onResize(self,*args):
        self.width=self.graph['width']
        self.height=self.graph['height']
    
    def _scale(self,y):
        yLim = 1.0-self.range(y)            # in [0,1]
        return round(self.size.height*yLim,0)
    
    @property
    def N(self):
        return len(self.points)
        
    def add(self,y):
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
          
        