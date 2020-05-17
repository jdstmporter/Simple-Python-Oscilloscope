'''
Created on 1 Apr 2020

@author: julianporter
'''
import sounddevice
import numpy
from .device import PCMDeviceSpecification


class PCMStreamCharacteristics(object):
    
    FORMATS = ['int8','uint8','int16','int32','float']
    
    
    def __init__(self,rate=48000,fmt='int16',blocksize=64):
        self.rate=rate
        self.format=fmt
        self.blocksize=blocksize
        
    def check(self,dev):
        sounddevice.check_input_settings(device=dev.index, dtype=self.format, samplerate=self.rate)
        
    
        
    

     
        
        
class PCMSessionDelegate(object):
    
    def __call__(self,n,time,data=[]):
        print(f'{n} {time}: {data}')

class PCMScale(object):
    
    def __init__(self,lower,upper):
        self.lower=lower
        self.upper=upper
        self.width=self.upper-self.lower
        self.factor=self.lower/self.width
        
        self.alpha = 2/(self.width)
        self.beta  = -(self.upper+self.lower)/self.width
        
    def limit(self,xs):
        return numpy.clip(xs,self.lower,self.upper)
    
    def scale(self,xs):
        return self.alpha * xs + self.beta
        

class PCMSession(object):
    
    RANGES = {
        'int8' :  128.0,
        'uint8' : 255.0,
        'int16' : 32768.0,
        'int32' : 4294967296.0,
        'float' : 1.0
    }  
    
    def __init__(self,specification : PCMDeviceSpecification, delegate : PCMSessionDelegate = PCMSessionDelegate()):
        self.specification=specification
        self.device=str(specification)
        self.name=specification.name
        self.index=specification.index
        #self.direction=specification.direction
        #self.channel=specification.channel
        self.delegate=delegate
        self.pcm = None
        self.data=[]
        self.scale=1.0
        
        
    @property
    def samplerate(self):
        return self.pcm.samplerate
 
    def callback(self,indata,frames,time,status):
        if status:
            print(f'Error: {status}')
        elif frames>0:
            #print(f'Scale {self.scale.lower} {self.scale.upper}')
            data=numpy.mean(indata,axis=1)/self.scale
            self.delegate(frames,time,data)

    @property
    def active(self):
        if self.pcm==None: return None
        return self.pcm.active        
        
    def start(self,characteristics = PCMStreamCharacteristics()):
        characteristics.check(self.specification)
        
        self.scale=PCMSession.RANGES[characteristics.format]
        self.pcm=sounddevice.InputStream(samplerate=characteristics.rate,blocksize=characteristics.blocksize,device=self.index,
                                            dtype=characteristics.format,callback=self.callback)
        self.pcm.start()
    
    
    def stop(self):
        if self.pcm: self.pcm.stop(True)
        self.pcm=None
        
    def kill(self):
        if self.pcm: self.pcm.abort(True)
        self.pcm=None