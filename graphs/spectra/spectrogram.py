'''
Created on 9 May 2020

@author: julianporter
'''

import tkinter as tk
import threading
import queue
import numpy as np
from util import SYSLOG, Range, DefaultTheme
from ..graphic import Graphic



NSTEPS=1000

class Runner(threading.Thread):
    def __init__(self, queue, average, offset, minimum, maximum,
                 gradient, xflen, height, callback):
        super().__init__()
        self.average=5
        self.offset=offset
        self.pos=0
        self.factor=1
        self.queue=queue
        self.callback=callback
        self.active=False
        self.ffts=np.zeros((self.average,xflen))
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
    
    def setRange(self,rnge):
        self.minimum=rnge.min
        self.maximum=rnge.max
        
    def setGradient(self,gradient):
        self.colours = [str(gradient(x/NSTEPS)) for x in range(NSTEPS+1)]

    def setSize(self, height):
        self.height=height
        factor=self.xflen/height
        
        mapping=[]
        for idx in range(height):
            offset=factor*idx
            start=int(offset)
            end=min(int(offset+factor)+1,self.xflen-1)
            mapping.append((start+end)//2)
        self.mapping=list(reversed(mapping))
        self.yRange=range(self.height-1,-1,-1)
        
        '''
        mapping=[0]
        for y in range(1, height):
            m = int(y*self.factor)
            if m > mapping[0]:
                mapping.insert(0,m)
        self.mapping=mapping
        '''

    def action(self, xformed):
        cols=[self.colour(xformed[idx]) for idx in self.mapping]
        #cols=[self.colour(0.5*(xformed[s]+xformed[e])) for s, e in self.mapping]
        self.callback(cols)

    def run(self):
        self.active=True
        self.pos=0
        while self.active:
            data=self.queue.get()
            self.action(data)

    def shutdown(self):
        self.active=False

class Spectrogram(Graphic):
    def __init__(self,root,bounds=Range(-1,1),theme=DefaultTheme,xflen=513):
        super().__init__(root,bounds,theme)
        
        self.width=800
        self.height=400
        self.sxFactor=10
        self.swidth=self.sxFactor*self.width
        self.gradient=theme.gradient
        self.photo=tk.PhotoImage(width=self.swidth,height=self.height)
        self.graph.config(scrollregion=(0,0,self.swidth,self.height))
        self.graph.create_image(0,0,anchor=tk.NW,image=self.photo,state='normal')
        
        self.scroll=tk.Scrollbar(self.root,orient=tk.HORIZONTAL)
        self.scroll.config(command=self.graph.xview)
        self.graph.config(xscrollcommand=self.scroll.set)
        
        print(f'Image size is ({self.photo.width()} x {self.photo.height()})')
        
        self.xflen=xflen
        self.xoffset=0
        self.ffts=[]

        self.queue=queue.Queue()
        self.thread=None
        self.average=2
        self.offset=1
        
    

    def start(self):
        def callback(data):
            self._plot(data)
        self.thread=Runner(self.queue,self.average,self.offset,self.range.min,self.range.max,
                           self.gradient,self.xflen,self.photo.height(),callback)
        self.thread.start()
        
    def stop(self):
        if self.thread:
            self.thread.shutdown()
            self.thread=None 
            
    def __call__(self,xformed):
        self.queue.put(xformed,block=False) 
        
    def shiftPage(self):
        origin=max((self.xoffset-self.width)/self.swidth,0)
        end=min(origin+self.width/self.swidth,1)
        self.graph.xview_moveto(origin)
        self.scroll.set(origin,end)
        
        
    def buildGUI(self):
        self.thread.setRange(self.range)
        self.xoffset=0
        self.shiftPage()
        self.photo.blank()
        super().buildGUI()
        
        
    def _plot(self,xformed):
        #print(f'Plotting at {self.xoffset} WRT {self.photo.width()}')
        self.photo.put(xformed,(int(self.xoffset),0))
        self.xoffset+=1 
        if self.xoffset > self.width:
            self.shiftPage()
           
    def configure(self,**kwargs):
        super().configure(**kwargs)
        if 'height' in kwargs:
            self.height=kwargs['height']
        if 'width' in kwargs:
            self.width=kwargs['width'] 
            self.swidth=int(self.width*self.sxFactor)
            kwargs['width'] = self.swidth
        self.graph.config(scrollregion=(0,0,self.swidth,self.height))
        self.photo.configure(width=self.swidth,height=self.height)
    
    
    def setGradient(self,gradient):
        self.gradient=gradient
        self.thread.setGradient(gradient)
