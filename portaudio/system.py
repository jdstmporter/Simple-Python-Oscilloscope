'''
Created on 1 Apr 2020

@author: julianporter
'''

import sounddevice
import itertools
from .direction import Direction
from .device import Dev, PCMDeviceSpecification

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
        c = cls._filtered(cutoff)
        return { d : cls._forDirection(d,c) for d in Direction.all() }
    
    
    def __init__(self,cutoff=8):
        self.cards = PCMSystem.loadCards(cutoff)
        self.devices  = PCMSystem.loadPCMs(cutoff) 
        
    def find(self,direction,index): 
        return [dev for dev in self.devices[direction] if dev.index==index]
        
    def __getitem__(self,card):
        if type(card) is str: card=self.cards[card]
        out = {}
        for direction in Direction.all:
            out[direction] = self.find(direction,card)
        return out
    
    def __call__(self):
        return self.devices
    
    
        
    
    def inputs(self,card):
        return [dev for dev in self[card][Direction.input]]
    
    def outputs(self,card):
        return [dev for dev in self[card][Direction.output]]
    
    
    def defaults(self,direction):
        key = PCMSystem.DEFAULT_KEYS[direction]
        indices = [api[key] for api in sounddevice.query_hostapis()]
        return itertools.chain(*[self.find(direction,idx) for idx in indices])
        
    
    @property
    def defaultInput(self):
        try: return self.defaults(Direction.input)[0]
        except: return None
        
    @property
    def defaultOutput(self):
        try: return self.defaults(Direction.output)[0]
        except: return None
            
            
        
        