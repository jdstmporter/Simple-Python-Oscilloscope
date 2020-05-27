'''
Created on 1 Apr 2020

@author: julianporter
'''

import sounddevice
from .device import Dev, PCMDeviceSpecification, Direction
from collections import OrderedDict

class API(object):
    
    DEFAULT_KEYS = { Direction.input  : 'default_input_device',
                     Direction.output : 'default_output_device'}
    NAME_KEY = 'name'
    DEVS_KEY = 'devices'
    IDX_KEY = 'index'
    
    def __init__(self,index=0,api={}):
        self._api=api
        self._api[API.IDX_KEY]=index
        
    def __getitem__(self,index):
        if index in Direction.all():
            index=API.DEFAULT_KEYS[index]
        return self._api[index]
    
    def __contains__(self,idx): return idx in self.devices
    def __iter__(self): return iter(self.devices)
    def __len__(self): return len(self.devices)
    
    @property
    def index(self): return self[API.IDX_KEY]
    @property
    def name(self): return self[API.NAME_KEY]
    @property
    def devices(self): return self[API.DEVS_KEY]
    @property
    def defaultIn(self): return self[Direction.input]
    @property
    def defaultOut(self): return self[Direction.output]
    
    @classmethod
    def load(cls):
        return [API(idx,api) for idx, api in enumerate(sounddevice.query_hostapis())]
    
        

class PCMSystem(object):
    
    DEFAULT_KEYS = { Direction.input  : 'default_input_device',
                     Direction.output : 'default_output_device'}
    
    @classmethod
    def _filtered(cls,cutoff=8):
        c = sounddevice.query_devices()
        devs = [Dev(d,idx) for idx, d in enumerate(c)]
        return [dev for dev in devs if dev.totalChannels <= cutoff]
    
       
    
    @classmethod
    def _forDirection(cls,direction=Direction.input,devs=[]):
        return [PCMDeviceSpecification(direction,dev) for dev in devs if dev.hasDirection(direction)]
              
    
    @classmethod
    def loadCards(cls,cutoff = 8):
        c = cls._filtered(cutoff)
        return { dev.name : dev.index for dev in c }
    
    @classmethod
    def loadPCMs(cls,cutoff=8):
        return  cls._filtered(cutoff)
    
    
    def __init__(self,cutoff=8):
        self.apis = API.load()
        self.apiIndices = [api.index for api in self.apis]
        self.cards = PCMSystem.loadCards(cutoff)
        self.devices  = PCMSystem.loadPCMs(cutoff) 
        
    def __getitem__(self,api):
        return [dev for dev in self.devices if dev.api == api]
    
    def inputs(self,api=0):
        return [dev for dev in self[api] if dev.hasDirection(Direction.input)]
    
    def outputs(self,api=0):
        return [dev for dev in self[api] if dev.hasDirection(Direction.output)]
    
    def defaults(self,direction,api=0):
        idx=self.apis[api][direction]
        return [dev for dev in self[api] if dev.index==idx]
        
    
    @property
    def defaultInput(self):
        try: return self.defaults(Direction.input)[0]
        except: return None
        
    @property
    def defaultOutput(self):
        try: return self.defaults(Direction.output)[0]
        except: return None
        
    @classmethod
    def devices(cls):
        pcm = PCMSystem()
        devs = OrderedDict()
        for dev in pcm.inputs():
            devs[dev.name] = dev
        return devs
        
            
            
        
        