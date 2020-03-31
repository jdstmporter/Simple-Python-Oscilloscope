'''
Created on 3 Mar 2020

@author: julianporter
'''

import alsaaudio

from typing import Mapping, Sequence

from .device import PCMDeviceSpecification
from .direction import Direction

    
DeviceSet = Mapping[Direction,Sequence[PCMDeviceSpecification]]

class DeviceSet(object):
    def __init__(self,cards={},pcms={}):
        self._devices={}
        for direction, devs in pcms.items():
            allDevs=[PCMDeviceSpecification(cards,dev,direction) for dev in devs]
            self._devices[direction]=[dev for dev in allDevs if dev.prefix=='hw'] 
        
    def __getitem__(self,direction):
        return self._devices.get(direction,[])
    
    def items(self):
        return self._devices.items()
    
    def inputs(self) -> DeviceSet:
        return self[Direction.input]
    
    def outputs(self) -> DeviceSet:
        return self[Direction.output]
        

class PCMSystem(object):
    
    @classmethod
    def loadCards(cls) -> Mapping[str,int]:
        c = alsaaudio.cards()
        return { card : index for index, card in enumerate(c) }
    
    @classmethod
    def loadPCMs(self) -> Mapping[Direction,Sequence[str]]:
        devs = {}
        for direction in Direction.all():
            devs[direction] = alsaaudio.pcms(direction.value)
        return devs
    
    def __init__(self):
        self.cards = PCMSystem.loadCards()
        self.pcms  = PCMSystem.loadPCMs() 
        
        self.devices = DeviceSet(cards=self.cards,pcms=self.pcms)
        
        
        
    def __getitem__(self,card) -> DeviceSet:
        if type(card) is str: card=self.cards[card]
        out = {}
        for direction, devs in self.devices.items():
            out[direction] = [dev for dev in devs if dev.index==card]
        return out
    
    def __call__(self):
        return self.devices
        
    
    def inputs(self,card) -> DeviceSet:
        return [dev for dev in self[card][Direction.input]]
    
    def outputs(self,card) -> DeviceSet:
        return [dev for dev in self[card][Direction.output]]
    
    
           
