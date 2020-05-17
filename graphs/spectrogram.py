'''
Created on 9 May 2020

@author: julianporter
'''

from .graphic import Range, Graphic
from .gradient import Gradient
from .spectra import SpectralBase
import tkinter as tk
import numpy as np

class Spectrogram(Graphic):
    
    def __init__(self,root,bounds=Range(-1,1),xscale=1,background='black',line='red',
                 gradient=Gradient(),xflen=513):
        super().__init__(root,bounds,xscale,background,line)
        
        self.gradient=gradient
        self.photo=tk.PhotoImage(width=800,height=400)
        self.graph.create_image(400,200,image=self.photo,state='normal')
        self.xflen=xflen
        self.xoffset=0
        self.ffts=[]
        
        self.average=4
        self.offset=2
        
    def _plot(self,xformed):
        w=self.photo.width()
        h=self.photo.height()
        factor=h/self.xflen
        x=int(self.xoffset)
        for y in range(h):
            f = int(y/factor)
            c=str(self.gradient(self.range(xformed[f])))
            #print(f'{c} @(0,{y}) with {w} {h} for {value} => {v}')
            self.photo.put(c,(x,h-y))
        self.xoffset+=1 
        
    def __call__(self,xformed):
        self.ffts.append(xformed)
        while len(self.ffts)>=self.average: 
            xformed=np.average(self.ffts[:self.average],axis=0)
            self.ffts=self.ffts[self.offset:]
            self._plot(xformed)
        
        
        
            
    def configure(self,**kwargs):
        super().configure(**kwargs)
        self.photo.configure(**kwargs)
            
        