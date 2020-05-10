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
    
    def __init__(self,size=1024,samplerate=48000):
        self.size=size
        self.samplerate=samplerate
        self.normaliser=10*np.log10(size*samplerate)
       
    @classmethod 
    def logNorm(cls,vector):
        return np.log2(np.absolute(vector))

    def powerSpectrum(self,data=[]):
        spec=np.fft.rfft(data,self.size)
        return 20*np.log10(np.absolute(spec))-self.normaliser
        
    
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
        
    def setSampleRate(self,rate=48000):
        self.fft=Transforms(self.fftSize,rate)
        
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
                xf.append(values[start:start+self.fftSize])
            chunk=np.average(xf,axis=0)
            xformed=self.fft.powerSpectrum(chunk)
            #ma = np.max(xformed)
            #mi = np.min(xformed)
            #print(f'{mi} <-> {ma}')
            for viewer in self.viewers: viewer(xformed)
    
    

            
        
        
        
        
        
        
        
        
        
        
        
