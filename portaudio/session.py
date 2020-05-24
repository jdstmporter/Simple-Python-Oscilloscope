'''
Created on 1 Apr 2020

@author: julianporter
'''
import sounddevice
import numpy as np
from .device import PCMDeviceSpecification
from util import SYSLOG


class PCMFormat(object):
    
    def __init__(self,name,minimum,maximum):
        self.name=name
        self.min=minimum
        self.max=maximum
        
        self.a=2.0/(maximum-minimum)
        self.b=-(maximum+minimum)/(maximum-minimum)
        
    def __str__(self):
        return self.name
    
    def __call__(self,values):
        return np.clip(values,self.min,self.max)*self.a - self.b

class PCMFormats(object):
    uint8 = PCMFormat('uint8',0,255)
    int8  = PCMFormat('int8',-128,127)
    int16 = PCMFormat('int16',-32768,32767)
    int32 = PCMFormat('int32',-4294967296,4294967295)
    float = PCMFormat('float',-1,1)
    
    @classmethod
    def get(cls,name):
        try:
            return getattr(PCMFormats,name)
        except:
            return None

class PCMStreamCharacteristics(object):
    
    FORMATS = ['int8','uint8','int16','int32','float']
    
    def __init__(self,rate=48000,fmt='int16',blocksize=64):
        self.rate=rate
        self.format=fmt
        self.blocksize=blocksize
        
        
        
    def check(self,dev):
        sounddevice.check_input_settings(device=dev.index, dtype=self.format, samplerate=self.rate)

        
class PCMData(object):
    
    def __init__(self,timestamp=None,data=np.array([])): 
        self.data=data[:]
        self.timestamp=timestamp
        
    @property
    def nChannels(self):
        return self.data.shape[1]
        
    def __call__(self):
        return np.mean(self.data,axis=1)
        
    def __getitem__(self,n):
        return self.data[:,n]
    
    def __len__(self):
        return self.data.shape[0]
    
    @property
    def mean(self):
        return np.mean(self())
               
        
class PCMSessionDelegate(object):
    
    def __call__(self,data):
        pass


class PCMSession(object):
       
    def __init__(self,specification : PCMDeviceSpecification, delegate : PCMSessionDelegate = PCMSessionDelegate()):
        self.specification=specification
        self.device=str(specification)
        self.name=specification.name
        self.index=specification.index
        self.delegate=delegate
        self.pcm = None
        self.data=[]
        self.format=None
        
        
    @property
    def samplerate(self):
        return self.pcm.samplerate
 
    def callback(self,indata,frames,time,status):
        if status:
            SYSLOG.info(f'{status} but got {frames} frames')
        elif frames>0:
            self.delegate(np.mean(indata,axis=1))

    @property
    def active(self):
        if self.pcm==None: return None
        return self.pcm.active        
        
    def start(self,characteristics = PCMStreamCharacteristics()):
        characteristics.check(self.specification)
        self.format=PCMFormats.get(characteristics.format)
        
        self.pcm=sounddevice.InputStream(samplerate=characteristics.rate,blocksize=characteristics.blocksize,device=self.index,
                                            dtype=characteristics.format,callback=self.callback)
        self.pcm.start()
    
    
    def stop(self):
        if self.pcm: self.pcm.stop(True)
        self.pcm=None
        
    def kill(self):
        if self.pcm: self.pcm.abort(True)
        self.pcm=None
        


