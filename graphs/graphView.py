'''
Created on 23 May 2020

@author: julianporter
'''
import numpy as np
from .viewBase import RunnerBase, ViewBase
from util import Range, DefaultTheme

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
                
    def __init__(self, root, bounds=Range(-1,1), theme = DefaultTheme,interval=20):
        super().__init__(root,bounds)
        self.interval = interval
        self.factor = 1
        self.setSampleRate()
        self.viewers=[]
        self.theme=theme
        
        
        
    def addViewer(self,klass,**kwargs):
        viewer=klass(self.root,self.range,self.theme,**kwargs)
        self.viewers.append(viewer)
        return viewer
    
    
    def setSampleRate(self, rate=48000):
        self.factor = rate//self.interval
        print(f'Rate is {rate}, interval is {self.interval}, factor is {self.factor}')
        
    def makeThread(self):
        def callback(data):
            #print(f'Data {data} viewers {self.viewers}')
            for viewer in self.viewers:
                viewer.add(data)
        return GraphView.Runner(self.queue, callback, self.factor)
    
    def configure(self, **kwargs):
        for v in self.viewers: 
            v.configure(**kwargs)
        
    def pack(self, **kwargs):
        for v in self.viewers: 
            v.pack(**kwargs)
        
    def grid(self,**kwargs):
        for v in self.viewers: 
            v.grid(**kwargs)
        
    def clear(self):
        for v in self.viewers: 
            v.clear()
