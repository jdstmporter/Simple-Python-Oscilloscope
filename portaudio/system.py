'''
Created on 1 Apr 2020

@author: julianporter
'''

import sounddevice
import itertools
from .direction import Direction
from .device import Dev, PCMDeviceSpecification

class PCMSystem(object):
    
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
        
    def __getitem__(self,card):
        if type(card) is str: card=self.cards[card]
        out = {}
        for direction, devs in self.devices.items():
            out[direction] = [dev for dev in devs if dev.index==card]
        return out
    
    def __call__(self):
        return self.devices
        
    
    def inputs(self,card):
        return [dev for dev in self[card][Direction.input]]
    
    def outputs(self,card):
        return [dev for dev in self[card][Direction.output]]
        
        