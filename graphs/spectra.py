'''
Created on 7 May 2020

@author: julianporter
'''
import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
from .graphic import Graphic,Range
from datetime import datetime

class Transforms(object):
    
    def __init__(self,size=1024):
        self.size=size
       
    @classmethod 
    def logNorm(cls,vector):
        return np.log2(np.absolute(vector))

    def powerSpectrum(self,data=[]):
        spec=np.fft.rfft(data,self.size)
        return Transforms.logNorm(spec)
        
    
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
    
class SpectralBase(object):
    def __init__(self,fftSize,average=5,overlap=0.5,viewers=[]):
        
        self.average = average
        self.overlap = overlap
        
        self.fft =Transforms(fftSize)
        self.buffer=[]
        self.fftSize=fftSize
        self.offset = int(fftSize*overlap)
        self.minpoints = fftSize + self.offset*(self.average-1)
        self.xflen = 1+fftSize//2
        
        self.viewers=viewers
        
    def plot(self,xformed):
        pass
        
    def add(self,values):
        self.buffer.extend(values)
        if len(self.buffer)>=self.minpoints:
            values = self.buffer[:self.minpoints]
            self.buffer=self.buffer[self.minpoints:]
            
            xf=[]
            for n in range(self.average):
                start=n*self.offset
                chunk=values[start:start+self.fftSize]
                xf.append(self.fft.powerSpectrum(chunk))
            xformed=np.mean(xf,0) 
            for viewer in self.viewers: viewer(xformed)
    
    

            
        
        
        
        
        
        
        
        
        
        
        
