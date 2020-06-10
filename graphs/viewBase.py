'''
Created on 22 May 2020

@author: julianporter
'''

from threading import Thread
from queue import Queue
from util import Range, SYSLOG

class RunnerBase(Thread):
    def __init__(self,queue,callback):
        super().__init__()
        self.buffer=[]
        self.queue=queue
        self.callback=callback
        self.active=False
        self.activated=False
        
        
    def process(self):
        pass
        
    def run(self):
        self.active=True
        while self.active:
            item=self.queue.get(block=True)
            if self.activated:
                self.buffer.extend(item)
                self.process()
    
    def shutdown(self):
        self.active=False  
        
    def activate(self,activated):
        self.activated=activated
        self.buffer.clear() 

class ViewBase(object):
    def __init__(self,root,bounds=Range(-1,1)):
        self.root=root
        self.range=bounds
        self.queue = Queue()
        self.thread = None
        self.viewers = []
        
    def setRange(self, rnge):
        self.range=rnge
        for viewer in self.viewers:
            SYSLOG.info(f'{self} : Setting range in {viewer} to {self.range}')
            viewer.setRange(self.range)
        
    def setSampleRate(self, rate=48000):
        pass
    
    
        
    def makeThread(self):
        pass
        
    def start(self):
        self.thread = self.makeThread()
        self.thread.start()

    def stop(self):
        if self.thread:
            self.thread.shutdown()
            self.thread = None
            
    def add(self, values):
        self.queue.put(values, block=False)
        
    def activate(self,status=True):
        SYSLOG.info(f'Changed active status of {self} to {status}')
        self.thread.activate(status)
        
    def configure(self, **kwargs):
        pass
    
    def pack(self):
        pass
    
    
    