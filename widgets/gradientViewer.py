'''
Created on 12 Jun 2020

@author: julianporter
'''

import tkinter as tk
from tkinter import ttk
from .configurable import GradientPickerDelegate
from util import DefaultTheme

class GradientViewer(tk.PhotoImage):
    
    def __init__(self,gradient,width,height,orientation=tk.HORIZONTAL):
        super().__init__(width=width,height=height)
        self.orientation=orientation
        self.gradient=gradient
        self.width=width
        self.height=height
        
    def buildGUI(self):
        self.blank()
        
        if self.orientation==tk.VERTICAL:
            cols = [str(self.gradient(1-(y/self.height))) for y in range(self.height)]
            for x in range(self.width):
                self.put(cols,(x,0))
        elif self.orientation==tk.HORIZONTAL:
            for x in range(self.width):
                colour=str(self.gradient(x/self.width))
                cols=[colour]*self.height
                self.put(cols,(x,0))
                
    def setGradient(self,gradient):
        self.gradient=gradient
        self.buildGUI()
        
    def setSize(self,w,h):
        self.width=w
        self.height=h
        self.buildGUI()
                
class GradientSelector(ttk.LabelFrame):
    
    def __init__(self,root=None,name='Gradient',theme=DefaultTheme):
        super().__init__(root,text=name)
        self.theme=theme 
        self.width=200
        self.height=40
        
        self.gradients=theme.gradients
        self.default=theme.gradient
        self.selected=tk.StringVar()
        self.selected.set(self.default.name)
        self.selector=ttk.Combobox(master=self,textvariable=self.selected,
                                   values=self.gradients.keys(),
                                   justify=tk.LEFT)
        self.selector.bind('<<ComboboxSelected>>', self.changed)
        
        self.canvas=tk.Canvas(master=self)
        self.viewer=None
        self.img=None
        
        #self.bind('<Configure>',lambda event : self.fixSize(event.width,event.height))
        
        
        self.selector.grid(row=0,column=0,sticky=(tk.N,tk.E, tk.W))
        self.canvas.grid(row=0,column=1,sticky=(tk.N,tk.E, tk.W))
        self.rowconfigure(0,weight=1)
        self.draw()
    
    def fixSize(self,w,h):
        self.width=w
        self.height=h
        print(f'Raw is ({w},{h}) - processed ({w//2},{h})')
        self.draw()
        
    def draw(self):
        self.configure(width=self.width,height=self.height)
        self.canvas.config(scrollregion=self.canvas.bbox(0,0,self.width//2,self.height))
        if self.img:
            self.canvas.delete(self.img)
        self.viewer=GradientViewer(self.gradient,self.width//2,self.height)
        self.viewer.buildGUI()
        self.img=self.canvas.create_image(0,0,anchor=tk.NW,image=self.viewer,state='normal')
         
        
    def changed(self,_=None):
        newGrad=self.gradients[self.selected.get()]
        if newGrad:
            self.viewer.setGradient(newGrad)
            for delegate in GradientPickerDelegate.instances():
                delegate.setGradient(newGrad)
            
    
    @property
    def gradient(self):
        return self.gradients[self.selected.get()]
        
        