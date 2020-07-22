'''
Created on 21 May 2020

@author: julianporter
'''
import numpy as np
import math



        
             
        


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
        #self.normaliser=10*np.log10(size) #10*np.log10(size*samplerate)
        self.average=average
    
    def powerSpectrum(self,data=[]):
        spec=np.fft.rfft(data,self.size)
        return Transforms.logNorm(spec)
    
    def spectralPhase(self,data=[],unwrap=True):
        spec=np.fft.rfft(data,self.size)
        if unwrap:
            return Transforms.unwrapPhase(spec)
        else:
            return np.angle(spec)
        
    
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