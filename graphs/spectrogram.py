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

NSTEPS=1000

class Runner(threading.Thread):
        
    def __init__(self,queue,average,offset,minimum,maximum,gradient,xflen,height,callback):
        super().__init__()
        self.average=average
        self.offset=offset
        self.ffts=[]
        self.queue=queue
        self.callback=callback
        self.active=False
        
        self.minimum=minimum
        self.maximum=maximum
        self.xflen=xflen
        print(f'Height is {height}')
        self.setSize(height)
        
        self.colours = [str(gradient(x/NSTEPS)) for x in range(NSTEPS+1)]
        
    def scale(self,value):
        clipped=np.clip(value,self.minimum,self.maximum)
        return (clipped-self.minimum)/(self.maximum-self.minimum)
    
    def colour(self,value):
        return self.colours[int(NSTEPS*self.scale(value))]
        
    def setSize(self,height):
        factor=self.xflen/height
        self.range=range(height)
        self.mapping=[int(y*factor) for y in range(height-1,-1,-1)]
        

    def action(self,xformed):
        self.ffts.append(xformed)
        while len(self.ffts)>=self.average: 
            value=np.average(self.ffts[:self.average],axis=0)
            self.ffts=self.ffts[self.offset:]
            cols = [self.colour(x) for x in value]
            cs = [[cols[self.mapping[y]]] for y in self.range]
            self.callback(cs)

            
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
        self.thread=Runner(self.queue,self.average,self.offset,self.range.min,self.range.max,
                           self.gradient,self.xflen,self.photo.height(),callback)
        self.thread.start()
        
    def stop(self):
        if self.thread:
            self.thread.shutdown()
            self.thread=None 
            
    def __call__(self,xformed):
        self.queue.put(xformed,block=False) 
       
 
        
    def _plot(self,xformed):

        #w=self.photo.width()
        #h=self.photo.height()
        #r=range(h-1,-1,-1)
        #factor=self.xflen/h
        x=int(self.xoffset)
        #cs = [[xformed[int(y*factor)]] for y in r]
        self.photo.put(xformed,(x,0))
        
        self.xoffset+=1 
     

           
    def configure(self,**kwargs):
        super().configure(**kwargs)
        self.photo.configure(**kwargs)
            
        