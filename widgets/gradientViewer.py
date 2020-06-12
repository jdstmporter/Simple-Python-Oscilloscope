'''
Created on 12 Jun 2020

@author: julianporter
'''

import tkinter as tk

class GradientViewer(tk.PhotoImage):
    
    def __init__(self,gradient,width,height,orientation=tk.HORIZONTAL,margin=0):
        super().__init__(width=width,height=height)
        self.orientation=orientation
        self.gradient=gradient
        self.margin=margin
        
    def buildGUI(self):
        self.blank()
        height=self.height()
        width=self.width()
        
        if self.orientation==tk.VERTICAL:
            offset = int(self.margin*width)
            cols = [str(self.gradient(1-(y/height))) for y in range(height)]
            for x in range(offset,width-offset):
                self.photo.put(cols,(x,0))
        elif self.orientation==tk.HORIZONTAL:
            cols = ['#000000']*height
            offset = int(self.margin*height)
            yrange = range(offset,height-offset)
            for x in range(width):
                colour=str(self.gradient(x/width))
                for y in yrange:
                    cols[y]=colour
                self.photo.put(cols,(x,0))
                
    def setGradient(self,gradient):
        self.gradient=gradient
        self.buildGUI()
                
                