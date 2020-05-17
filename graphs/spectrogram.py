'''
Created on 9 May 2020

@author: julianporter
'''

from .graphic import Range, Graphic
from .gradient import Gradient
import tkinter as tk
import numpy as np
import threading
import queue

class Runner(threading.Thread):
        
    def __init__(self,queue,average,offset,callback):
        super().__init__()
        self.average=average
        self.offset=offset
        self.ffts=[]
        self.queue=queue
        self.callback=callback
        self.active=False
        
    def setSize(self,width,height):
        self.width=width
        self.height=height
        

    def action(self,xformed):
        self.ffts.append(xformed)
        while len(self.ffts)>=self.average: 
            value=np.average(self.ffts[:self.average],axis=0)
            self.ffts=self.ffts[self.offset:]
            self.callback(value)

            
    def run(self):
        self.active=True
        while self.active:
            data=self.queue.get()
            self.action(data)
            
    def shutdown(self):
        self.active=False

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
        
        self.queue=queue.Queue()
        self.thread=None
        self.average=2
        self.offset=1
        
   
    
    def start(self):
        def callback(xf):
            self._plot(xf)
        self.thread=Runner(self.queue,self.average,self.offset,callback)
        self.thread.start()
        
    def stop(self):
        if self.thread:
            self.thread.shutdown()
            self.thread=None 
            
    def __call__(self,xformed):
        self.queue.put(xformed,block=False) 
       
 
        
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
     

           
    def configure(self,**kwargs):
        super().configure(**kwargs)
        self.photo.configure(**kwargs)
            
        