'''
Created on 21 May 2020

@author: julianporter
'''
import numpy as np


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
        spec = np.log10(np.fft.fft(data,self.size))
        return np.fft.ifft(spec,self.size)

    def powerRCepstrum(self,data=[]):
        return Transforms.logNorm(self.rCepstrum(data))

    def powerCxCepstrum(self,data=[]):
        return Transforms.logNorm(self.cxCepstrum(data))