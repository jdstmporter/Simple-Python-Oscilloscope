'''
Created on 7 Mar 2020

@author: julianporter
'''

from itertools import chain
import numpy as np
from .graphic import Graphic
from util import Range


from graphs.viewBase import RunnerBase, ViewBase
        
        
class Graph(Graphic):
    
    def __init__(self,root,bounds=Range(-1,1),background='black',line='red'):
        super().__init__(root,bounds,background,line)
        self.basePoints=[-1,self.height,-1,self.height]
        self.line = self.graph.create_line(*self.basePoints,fill=line)
       
    def bind(self,binding,callback):
        self.graph.bind(binding,callback)
        
    def grid(self,**kwargs):
        self.graph.grid(**kwargs)
  
    def fixSize(self):
        s=self.size
        if s.width!=self.width:
            self.width=s.width
            self.xs=list(range(0,self.width))
        self.height=s.height
    
    def __len__(self):
        return len(self.points)
        
    def add(self,y):
        self.fixSize()
        
        y=(1.0-self.range(y))*self.height
        self.ys=(self.ys+[y])[-self.width:]
        points=list(chain(*zip(self.xs,self.ys)))
        if len(self.ys)>=2:
            self.graph.coords(self.line,points)
        
        
        
    def clear(self):
        self.ys=[]
        self.graph.coords(self.line,self.basePoints)
        
class GraphView(ViewBase):
    class Runner(RunnerBase):
        def __init__(self,queue,callback,factor):
            super().__init__(queue,callback)
            self.factor=factor
            print(f'Factor is {factor}')
            
        def process(self):
            while len(self.buffer)>=self.factor:
                values = self.buffer[:self.factor]
                self.buffer=self.buffer[self.factor:]
                value = np.mean(np.square(values))
                decibels = 5.0*np.log10(value) - 10.0*np.log10(32768.0)
                self.callback(decibels)
                
    def __init__(self, root, bounds=Range(-1,1), background='black', line='red',interval=20):
        super().__init__(root,bounds)
        self.interval = interval
        self.factor = 1
        self.graph = Graph(self.root,bounds=bounds,background=background,line=line)
        self.setSampleRate()
    
    
    def setSampleRate(self, rate=48000):
        self.factor = rate//self.interval
        print(f'Rate is {rate}, interval is {self.interval}, factor is {self.factor}')
        
    def makeThread(self):
        def callback(data):
            self.graph.add(data)
        return GraphView.Runner(self.queue, callback, self.factor)
    
    def configure(self, **kwargs):
        self.graph.configure(**kwargs)
        
    def pack(self, **kwargs):
        self.graph.pack(**kwargs)
        
    def grid(self,**kwargs):
        self.graph.grid(**kwargs)
        
    def clear(self):
        self.graph.clear()
          
        