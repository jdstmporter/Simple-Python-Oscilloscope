'''
Created on 1 Apr 2020

@author: julianporter
'''
import sounddevice
import numpy
from .device import PCMDeviceSpecification
from .ranges import Range

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


class PCMSession(object):
    
    RANGES = {
        'int8' : (-128,127),
        'uint8' : (0,255),
        'int16' : (-32768,32767),
        'int32' : (-0x100000000,0xffffffff),
        'float' : (-1,1)
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
        self.range=Range()
        
        
    @property
    def samplerate(self):
        return self.pcm.samplerate
 
    def callback(self,indata,frames,time,status):
        if status:
            print(f'Error: {status}')
        elif frames>0:
            data=self.range(numpy.mean(indata,axis=1))
            self.delegate(frames,time,data)

    @property
    def active(self):
        if self.pcm==None: return None
        return self.pcm.active        
        
    def start(self,characteristics = PCMStreamCharacteristics()):
        characteristics.check(self.specification)
        
        self.range=Range(PCMSession.RANGES[characteristics.format])
        self.pcm=sounddevice.InputStream(samplerate=characteristics.rate,blocksize=characteristics.blocksize,device=self.index,
                                            dtype=characteristics.format,callback=self.callback)
        self.pcm.start()
    
    
    def stop(self):
        if self.pcm: self.pcm.stop(True)
        self.pcm=None
        
    def kill(self):
        if self.pcm: self.pcm.abort(True)
        self.pcm=None