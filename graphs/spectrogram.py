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
from util import SYSLOG

NSTEPS=1000

class Runner(threading.Thread):
        
    def __init__(self,queue,average,offset,minimum,maximum,gradient,xflen,height,callback):
        super().__init__()
        self.average=average
        self.offset=offset
        self.ffts=np.zeros(xflen)
        self.queue=queue
        self.callback=callback
        self.active=False
        
        self.minimum=minimum
        self.maximum=maximum
        self.xflen=xflen
        SYSLOG.info(f'Height is {height}')
        self.setSize(height)
        
        
        
        self.colours = [str(gradient(x/NSTEPS)) for x in range(NSTEPS+1)]
        
    def scale(self,value):
        clipped=np.clip(value,self.minimum,self.maximum)
        return (clipped-self.minimum)/(self.maximum-self.minimum)
    
    def colour(self,value):
        return self.colours[int(NSTEPS*self.scale(value))]
        
    def setSize(self,height):
        factor=self.xflen/height
        mapping=[0]
        for y in range(1,height):
            m=int(y*factor)
            if m > mapping[0]: 
                mapping.insert(0,m)
        self.mapping=mapping
        

    def action(self,xformed):
        self.ffts = 0.8*xformed + 0.2*self.ffts
        #np.copyto(self.ffts[self.ringOffset],xformed)
        #self.ringOffset = 1 - self.ringOffset
         
        #value=np.average(self.ffts,axis=0)
        cols = [self.colour(self.ffts[m]) for m in self.mapping]
        self.callback(cols)

            
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
        self.photo.put(xformed,(int(self.xoffset),0))
        self.xoffset+=1 
     

           
    def configure(self,**kwargs):
        super().configure(**kwargs)
        self.photo.configure(**kwargs)
            
        