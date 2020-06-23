'''
Created on 12 Jun 2020

@author: julianporter
'''

import tkinter as tk
from tkinter import ttk
from .configurable import GradientPickerDelegate
from util import DefaultTheme


                
class GradientSelector(ttk.LabelFrame):
    
    def __init__(self,root=None,name='Gradient',theme=DefaultTheme):
        super().__init__(root,text=name)
        self.theme=theme 
        self.width=200
        self.height=40
        
        self.listeners=[]
        
        self.gradients=theme.gradients
        self.default=theme.gradient
        self.selected=tk.StringVar()
        self.selected.set(self.default.name)
        self.selector=ttk.Combobox(master=self,textvariable=self.selected,
                                   values=self.gradients.keys(),
                                   justify=tk.LEFT)
        
        
        self.canvas=tk.Canvas(master=self)
        self.viewer=tk.PhotoImage(width=self.width,height=self.height)
        self.canvas.create_image(0,0,anchor=tk.NW,image=self.viewer,state='normal')
        self.canvas.configure(width=self.width//2,height=self.height)
        
        self.selector.bind('<<ComboboxSelected>>', self.changed)
        self.bind('<Configure>',lambda event : self.fixSize(event.width,event.height))
        
        
        self.selector.grid(row=0,column=0,sticky=(tk.E, tk.W))
        self.canvas.grid(row=0,column=1,sticky=(tk.N, tk.S, tk.E, tk.W))
        self.rowconfigure(0,weight=1)
        
    def addListeners(self,*args):
        self.listeners.extend(args)
        
    def draw(self):
        w=self.width//2
        print(f'Width = {w} Height = {self.height}')
        for x in range(w):
            colour=str(self.gradient(x/w))
            cols=[colour]*self.height
            self.viewer.put(cols,(x,0))
    
    def fixSize(self,w,h):
        self.width=w
        self.height=h
        print(f'Raw is ({w},{h}) - processed ({w//2},{h})')
        self.canvas.configure(scrollregion=self.canvas.bbox(0,0,self.width//2,self.height))
        self.draw()
        
    def changed(self,_=None):
        newGrad=self.gradients[self.selected.get()]
        if newGrad:
            self.draw()
            for delegate in self.listeners:
                delegate.setGradient(newGrad)
            
    
    @property
    def gradient(self):
        return self.gradients[self.selected.get()]
        
        