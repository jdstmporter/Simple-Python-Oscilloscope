'''
Created on 9 May 2020

@author: julianporter
'''

from .graphic import Graphic, Range
from .gradient import Gradient
import tkinter as tk
import numpy as np

class Spectrogram(Graphic):
    
    def __init__(self,root,bounds=Range(-1,1),xscale=1,background='black',line='red',
                 gradient=Gradient(),xflen=513):
        super().__init__(root,bounds,xscale,background,line)
        
        self.graph.config(scrollregion=(0,0,3200,400))
        self.graph.pack(side=tk.TOP,fill=tk.BOTH)
        self.scroller = tk.Scrollbar(self.root,orient=tk.HORIZONTAL)
        self.scroller.pack(side=tk.BOTTOM, fill=tk.X)
        self.graph.configure(xscrollcommand=self.scroller.set)
        self.scroller.configure(command=self.scroll)
        self.gradient=gradient
        self.photo=tk.PhotoImage(width=3200,height=400)
        self.graph.create_image(400,200,image=self.photo,state='normal')
        self.xflen=xflen
        
        self.average=10
        
        self.ffts=[]
        
    def scroll(self,*args):
        print(*args)
        self.graph.xview(*args)
        
        
    def __call__(self,xformed):
        self.ffts.append(xformed)
        h=self.photo.height()
        factor=h/self.xflen
        x=len(self.ffts)-1
        for y in range(h):
            f = int(y/factor)
            c=str(self.gradient(self.range(xformed[f])))
            #print(f'{c} @(0,{y}) with {w} {h} for {value} => {v}')
            self.photo.put(c,(x,h-y))
            
    def configure(self,**kwargs):
        super().configure(**kwargs)
        self.photo.configure(**kwargs)
        
    def clear(self):
        self.ffts=[]
            
        