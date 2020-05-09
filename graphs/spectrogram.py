'''
Created on 9 May 2020

@author: julianporter
'''

from .graphic import Range, Graphic
from .gradient import Gradient
from .spectra import SpectralBase
import tkinter as tk

class Spectrogram(Graphic):
    
    def __init__(self,root,bounds=Range(-1,1),xscale=1,background='black',line='red',
                 gradient=Gradient.greyscale(),xflen=513):
        super().__init__(root,bounds,xscale,background,line)
        
        self.gradient=gradient
        self.photo=tk.PhotoImage(width=800,height=300)
        self.graph.create_image(400,150,image=self.photo,state='normal')
        self.xflen=xflen
        self.xoffset=0
        
    def __call__(self,xformed):
        w=self.photo.width()
        h=self.photo.height()
        factor=h/self.xflen
        x=int(self.xoffset)
        for idx, value in enumerate(xformed):
            c=str(self.gradient(self.range(value)))
            y=int(idx*factor)
            #print(f'{c} @(0,{y}) with {w} {h} for {value} => {v}')
            self.photo.put(c,(x,y))
        self.xoffset+=1
            
    def configure(self,**kwargs):
        super().configure(**kwargs)
        self.photo.configure(**kwargs)
            
        