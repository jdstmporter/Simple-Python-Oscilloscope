'''
Created on 21 May 2020

@author: julianporter
'''

from .spectra import Spectrogram, SpectrumView 
import threading
import queue
import tkinter as tk

from util import Transforms, Range, Gradient


class SpectralView(object):
    
    class Runner(threading.Thread):
    
        def __init__(self,queue,callback,fft,fftSize,average):
            super().__init__()
            self.buffer=[]
            self.queue=queue
            self.callback=callback
            self.fft=fft
            self.fftSize=fftSize
            self.active=False
            self.average=average
            self.ffts=[]
            
        def run(self):
            self.active=True
            while self.active:
                item=self.queue.get(block=True)
                self.buffer.extend(item)
                while len(self.buffer)>=self.fftSize:
                    values = self.buffer[:self.fftSize]
                    self.buffer=self.buffer[self.fftSize:]
                    self.callback(self.fft.powerSpectrum(values))
                                      
        def shutdown(self):
            self.active=False
    
    def __init__(self,root,bounds=Range(-1,1),xscale=1,background='black',line='red',
                 gradient=Gradient(),fftSize=1024,average=10):
        
        self.root=root
        self.range=bounds
        self.xscale=xscale
        
        self.queue = queue.Queue()
        self.thread=None
        self.average=average
        
        
        self.fft =Transforms(fftSize)
        self.fftSize=fftSize
        self.xflen = 1+fftSize//2
        
        self.spectrogram=Spectrogram(self.root,self.range,self.xscale,background,line,gradient,self.xflen)
        self.spectrum=SpectrumView(self.root,self.range,self.xscale,background,line,self.xflen)
        self.viewers=[self.spectrum,self.spectrogram]
        
    def setSampleRate(self,rate=48000):
        self.fft=Transforms(self.fftSize,rate)
        
    def start(self):
        self.spectrogram.start()
        def callback(xf):
            #self.ffts.append(xf)
            for viewer in self.viewers: viewer(xf)
        self.thread=SpectralView.Runner(self.queue,callback,self.fft,self.fftSize,self.average)
        self.thread.start()
        
    def stop(self):
        if self.thread:
            self.thread.shutdown()
            self.thread=None
        self.spectrogram.stop()
        
        
    def add(self,values):
        self.queue.put(values,block=False)

        
    def configure(self,width=0,height=0):
        self.spectrogram.configure(width=int(0.8*width),height=height)
        self.spectrum.configure(width=int(0.2*width),height=height)
        
    def pack(self):
        self.spectrogram.grid(column=0, row=0, sticky=(tk.N,tk.S,tk.E,tk.W))
        self.spectrogram.graph.config(scrollregion=self.spectrogram.graph.bbox(tk.ALL))
        self.spectrum.grid(column=1, row=0, sticky=(tk.N,tk.S,tk.E,tk.W))
  
