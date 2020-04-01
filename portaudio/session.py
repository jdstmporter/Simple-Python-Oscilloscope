'''
Created on 1 Apr 2020

@author: julianporter
'''
import sounddevice
import numpy
from .device import PCMDeviceSpecification



class PCMSessionDelegate(object):
    
    def __call__(self,n,time,data=[]):
        print(f'{n} {time}: {data}')


class PCMSession(object):
    
    def __init__(self,specification : PCMDeviceSpecification, delegate : PCMSessionDelegate = PCMSessionDelegate()):
        self.device=str(specification)
        self.name=specification.name
        self.index=specification.index
        self.direction=specification.direction
        #self.channel=specification.channel
        self.delegate=delegate
        self.pcm = None
        self.data=[]
 
    def callback(self,indata,frames,time,status):
        if status:
            print(f'Error: {status}')
        elif frames>0:
            data=numpy.sum(indata,axis=0)
            self.delegate(frames,time,data)

    @property
    def active(self):
        if self.pcm==None: return None
        return self.pcm.active        
        
    def start(self,pcmFormat = 'int16', rate = 48000,blocksize=64):
        
        self.pcm=sounddevice.InputStream(samplerate=rate,blocksize=blocksize,device=self.index,
                                            dtype=pcmFormat,callback=self.callback)
        self.pcm.start()
    
    
    def stop(self):
        if self.pcm: self.pcm.stop(True)
        self.pcm=None
        
    def kill(self):
        if self.pcm: self.pcm.abort(True)
        self.pcm=None