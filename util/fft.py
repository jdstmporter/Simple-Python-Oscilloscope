'''
Created on 21 May 2020

@author: julianporter
'''
import numpy as np
import math
from collections import namedtuple


        
             
      
SpectralData = namedtuple('SpectralData',['modulus','phase'])

class Transforms(object):
    
    EPSILON = 1.0e-50
    
    @classmethod
    def unwrapPhase(cls,vector):
        last=1+0j
        sheet=0
        out=[]
        for z in vector:
            if np.real(last)<0 and np.real(z)<0:
                if np.imag(last)>0 and np.imag(z)<0:
                    sheet+=2*math.pi
                elif np.imag(last)<0 and np.imag(z)>0:
                    sheet-=2*math.pi
            out.append(np.angle(z)+sheet)
            last = z
        return out
 
    @classmethod
    def logNorm(cls,vector):
        normed=np.absolute(vector)
        return 20*np.log10(normed+Transforms.EPSILON)  #-self.normaliser
     
    def __init__(self,size=1024,average=10):
        self.size=size
        self.xflen=1+size//2
        self.half=size//2
        #self.normaliser=10*np.log10(size) #10*np.log10(size*samplerate)
        self.average=average
        self.multiples=10
        self.RMS=0
    
    def powerSpectrum(self,data=[]):
        return self.spectrum(data)[0]
    
    def spectralPhase(self,data=[]):
        phases=self.spectrum(data)[1]
        evens=phases[0::2]
        odds=-np.append(phases[1::2],[0])
        return np.concatenate(np.stack((evens,odds),axis=1))[:-1]
    
    def rms(self,first,second):
        r = np.sqrt(np.mean(np.multiply(first,first)))
        s = np.sqrt(np.mean(np.multiply(second,second)))
        self.RMS = 0.8*(0.55*r + 0.45*s) + 0.2*self.RMS
        return self.RMS
        
    def autocorrelate(self,data=[]):
        first, second = np.split(np.array(data),2)
        c1=np.correlate(first,first,mode='full')[:self.xflen]   
        c2=np.correlate(second,second,mode='full')[:self.xflen]   
        return 0.5*(c1+c2)/(self.rms(first,second)+Transforms.EPSILON)
        
    
    def spectrum(self,data=[]):
        spec=np.fft.rfft(data,self.size)
        return (Transforms.logNorm(spec),np.angle(spec))
    
    
    def cepstrum(self,data=[]):
        reals = Transforms.logNorm(np.fft.rfft(data,self.size))
        inv = np.fft.irfft(reals,self.size)
        flipped = np.flip(inv)+inv
        return flipped[:self.xflen]
    
