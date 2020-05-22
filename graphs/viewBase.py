'''
Created on 22 May 2020

@author: julianporter
'''

from threading import Thread
from queue import Queue
import tkinter as tk
from util import Range

class RunnerBase(Thread):
    def __init__(self,queue,callback):
        super().__init__()
        self.buffer=[]
        self.queue=queue
        self.callback=callback
        self.active=False
        
    def process(self):
        pass
        
    def run(self):
        self.active=True
        while self.active:
            item=self.queue.get(block=True)
            self.buffer.extend(item)
            self.process()
    
    def shutdown(self):
        self.active=False   

class ViewBase(object):
    def __init__(self,root,bounds=Range(-1,1)):
        self.root=root
        self.range=bounds
        self.queue = Queue()
        self.thread = None
        
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
        
    def configure(self, width=0, height=0):
        pass
    
    def pack(self):
        pass
    