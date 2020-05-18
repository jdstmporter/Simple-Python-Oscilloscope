'''
Created on 7 May 2020

@author: julianporter
'''
import numpy as np
import threading
import queue
from math import log10



class Transforms(object):
    
    EPSILON = 1.0e-10
    
    def __init__(self,size=1024,samplerate=48000,average=10):
        self.size=size
        self.samplerate=samplerate
        self.normaliser=10*np.log10(size*samplerate)
        self.average=average
       
    def logNorm(self,vector):
        return 20*np.log10(np.absolute(vector)+Transforms.EPSILON)-self.normaliser

    def powerSpectrum(self,data=[]):
        spec=np.fft.rfft(data,self.size)
        return self.logNorm(spec)
        
    
    def rCepstrum(self,data=[]):
        reals = self.powerSpectrum(data)
        return np.fft.irfft(reals,self.size)
    
    def cxCepstrum(self,data=[]):
        spec = np.log2(np.fft.fft(data,self.size))
        return np.fft.ifft(spec,self.size)

    def powerRCepstrum(self,data=[]):
        return Transforms.logNorm(self.rCepstrum(data))

    def powerCxCepstrum(self,data=[]):
        return Transforms.logNorm(self.cxCepstrum(data))
    
class SpectralRunner(threading.Thread):
    
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
            item=self.queue.get()
            self.buffer.extend(item)
            while len(self.buffer)>=self.fftSize:
                values = self.buffer[:self.fftSize]
                self.buffer=self.buffer[self.fftSize:]
                self.callback(self.fft.powerSpectrum(values))
                            
            

            
    def shutdown(self):
        self.active=False
    
class SpectralBase(object):
    def __init__(self,fftSize,average=10,viewers=[]):
        
        self.queue = queue.Queue()
        self.thread=None
        self.average=average
        
        
        self.fft =Transforms(fftSize)
        self.fftSize=fftSize
        self.xflen = 1+fftSize//2
        
        self.viewers=viewers
        #self.ffts=[]
        
    def setSampleRate(self,rate=48000):
        self.fft=Transforms(self.fftSize,rate)
        
        
    def start(self):
        def callback(xf):
            #self.ffts.append(xf)
            for viewer in self.viewers: viewer(xf)
        self.thread=SpectralRunner(self.queue,callback,self.fft,self.fftSize,self.average)
        self.thread.start()
        
    def stop(self):
        if self.thread:
            self.thread.shutdown()
            self.thread=None
        
    def add(self,values):
        self.queue.put(values,block=False)
'''        self.buffer.extend(values)
        if len(self.buffer)>=self.fftSize:
            chunk = self.buffer[:self.fftSize]
            self.buffer=self.buffer[self.fftSize:]
#        if len(self.buffer)>=self.minpoints:
#            values = self.buffer[:self.minpoints]
#            self.buffer=self.buffer[self.minpoints:]           
#            xf=[]
#            for n in range(self.average):
#                start=n*self.offset
#                xf.append(values[start:start+self.fftSize])
#            chunk=np.average(xf,axis=0)
            xformed=self.fft.powerSpectrum(chunk)
            #ma = np.max(xformed)
            #mi = np.min(xformed)
            #print(f'{mi} <-> {ma}')
            for viewer in self.viewers: viewer(xformed)
'''    
    

            
        
        
        
        
        
        
        
        
        
        
        
