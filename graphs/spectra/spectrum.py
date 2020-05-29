'''
Created on 9 May 2020

@author: julianporter
'''
import tkinter as tk
import numpy as np
from util import Range, DefaultTheme
from ..graphic import Graphic


        

class SpectrumView(Graphic):

    def __init__(self, root, bounds=Range(-1,1), theme=DefaultTheme, xflen=513):
        super().__init__(root, bounds, theme)
        self.line = self.graph.create_line(-1, 0, -1, 0, **theme.spectrum)
        self.xflen = xflen
        self.points = [0]*2*self.xflen
        self.average=5
        self.pos=0
        self.ffts=np.zeros((self.average,xflen))
        

        
    def yval(self,value):
        return (1-self.range(value))*self.height
        
    def buildGUI(self):
        super().buildGUI()
        box=self.graph.create_rectangle(0,0,self.width-1,self.height-1,**self.theme.axes)
        self.axes=[box]
        
        
        
        
        # do left hand markers
        interval=20
        bot, top = self.range.closure(width=interval).int()
        marks = list(range(bot,top+1,interval))
        for mark in marks:
            y=self.yval(mark)
            text=self.graph.create_text(self.width-2,y,text=str(mark),
                                        anchor=tk.E,justify=tk.RIGHT,
                                        **self.theme.labels)
            
            line = self.graph.create_line(0,y,self.width-1,y,**self.theme.grid(mark==0))
            self.axes.extend([text,line])
            
        

    def fixSize(self,w,h):
        if w != self.width:
            self.width=w
            xscale = w / self.xflen
            for idx in range(self.xflen):
                self.points[2*idx] = idx*xscale
        self.height = h
        self.buildGUI()
        
        '''if s.height != self.height:
            self.height=s.height
            yscale = s.height / self.xflen
            for n in range(self.xflen): self.points[2*n+1]=self.height-n*yscale
        self.width=s.width'''


    def __call__(self,xformed):
        values=xformed #self.windower(xformed)
        for index,value in enumerate(values):
            yVal = (1-self.range(value))*self.height
            self.points[2*index+1] = yVal
            ''''x=self.range(value)*self.width
            self.points[2*index]=x'''
        self.graph.coords(self.line, self.points)


