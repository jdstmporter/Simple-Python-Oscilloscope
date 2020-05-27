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
        
        self.divisor=np.max(np.abs([self.min,self.max]))
        
    def __str__(self):
        return self.name
    
    def __call__(self,values):
        return np.clip(values,self.min,self.max)*self.a - self.b
    

class PCMStreamCharacteristics(object):
    
    FORMATS = {
        'uint8': PCMFormat('uint8',0,255),
        'int8' : PCMFormat('int8',-128,127),
        'int16': PCMFormat('int16',-32768,32767),
        'int32': PCMFormat('int32',-4294967296,4294967295),
        'float': PCMFormat('float',-1,1)
    }
    
    def __init__(self,rate=48000,fmt='int16',blocksize=64):
        self.rate=rate
        self.format=fmt
        self.blocksize=blocksize
        
        
        
    def check(self,dev):
        sounddevice.check_input_settings(device=dev.index, dtype=self.format, samplerate=self.rate)


class PCMSessionDelegate(object):
    
    def __call__(self,data):
        pass
    
    def connect(self,samplerate):
        pass
    
    def startListeners(self):
        pass
    
    def stopListeners(self):
        pass

class PCMSessionHandler(object):
    def __init__(self,delegate=PCMSessionDelegate()):
        self.pcm=None
        self.format=None
        self.delegate=delegate
        
    def connect(self,dev):
        try:
            if self.pcm:
                self.stop()
            self.pcm=PCMSession(dev,delegate=self.delegate)
            self.delegate.connect(self.pcm.samplerate)          
        except Exception as ex:
            SYSLOG.error(f'{ex}')
            
    def disconnect(self):
        try:
            if self.pcm:
                self.stop()
                self.pcm=None
        except Exception as ex:
            SYSLOG.error(f'{ex}')
            
    def start(self):
        self.delegate.startListeners()
        self.pcm.start()
        self.format=self.pcm.format
        SYSLOG.info(f'Started {self.pcm}')
        
        
    def stop(self):
        if self.pcm:
            self.pcm.stop()
            self.format=None
        self.delegate.stopListeners()
    
    
            
  

class PCMSession(object):
    
    '''
    class Formatter(threading.Thread):
        def __init__(self,queue,formatter,delegate):
            super().__init__()
            self.queue=queue
            self.formatter=formatter
            self.delegate=delegate
            self.active=False
            self.last=[]

        def run(self):
            self.active=True
            while self.active:
                data=self.queue.get(block=True)
                data=self.formatter(np.mean(data,axis=1))
                self.delegate(data)
                
        def shutdown(self):
            self.active=False
    '''
                
       
    def __init__(self,specification : PCMDeviceSpecification, delegate : PCMSessionHandler = PCMSessionHandler()):
        self.specification=specification
        self.device=str(specification)
        self.name=specification.name
        self.index=specification.index
        self.delegate=delegate
        self.pcm = None
        self.format=None
        #self.queue=Queue()
        #self.thread=None
        
        
    @property
    def samplerate(self):
        return self.pcm.samplerate
 
    def callback(self,indata,frames,time,status):
        if status:
            SYSLOG.info(f'{status} but got {frames} frames')
        elif len(indata)>0:
            self.delegate(np.mean(indata,axis=1)/self.format.divisor)
            #self.queue.put(indata[:],block=False)
            #self.delegate(np.mean(indata,axis=1))

    @property
    def active(self):
        if self.pcm==None: return None
        return self.pcm.active        
        
    def start(self,characteristics = PCMStreamCharacteristics()):
        characteristics.check(self.specification)
        self.format=PCMStreamCharacteristics.FORMATS.get(characteristics.format)
        
        #self.thread = PCMSession.Formatter(self.queue,self.format,self.delegate)
        #self.thread.start()
        
        self.pcm=sounddevice.InputStream(samplerate=characteristics.rate,blocksize=characteristics.blocksize,device=self.index,
                                            dtype=characteristics.format,callback=self.callback)
        self.pcm.start()
    
    
    def stop(self):
        if self.pcm: self.pcm.stop(True)
        self.pcm=None
        #if self.thread:
        #    self.thread.shutdown()
        #    self.thread = None
        
    def kill(self):
        if self.pcm: self.pcm.abort(True)
        self.pcm=None
        #if self.thread:
        #    self.thread.shutdown()
        #    self.thread = None
        


