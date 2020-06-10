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
        
        
    @property
    def size(self):
        return Size(int(self.graph['width']),int(self.graph['height']))
    
    def yval(self,value):
        return (1-self.range(value))*self.height
    
    def xval(self,value):
        return self.range(value)*self.width
    
    def fixSize(self,w,h):
        pass
    
    def buildGUI(self):
        for item in self.axes:
            self.graph.delete(item)
        box=self.graph.create_rectangle(0,0,self.width-1,self.height-1,**self.theme.axes)
        self.axes=[box]  
        
    def makeGrid(self,interval=10,orientation=tk.VERTICAL):

        bot, top = self.range.closure(width=interval).int()
        marks = list(range(bot,top+1,interval))
        for mark in marks:
            if orientation==tk.VERTICAL:
                x=self.xval(mark)
                xy=[x,self.height-2]
                xyxy=[x,0,x,self.height-1]
                anchor=tk.S
            else:
                y=self.yval(mark)
                xy=[2,y]
                xyxy=[0,y,self.width-1,y]
                anchor=tk.W
            text=self.graph.create_text(*xy,text=str(mark),
                                        anchor=anchor,justify=tk.RIGHT,
                                        **self.theme.labels)
            
            line = self.graph.create_line(*xyxy,**self.theme.grid(mark==0))
            self.axes.extend([text,line]) 
    
    def setRange(self,rnge):
        self.range=rnge
        self.buildGUI()
        
    
    
     
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

