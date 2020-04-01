'''
Created on 1 Apr 2020

@author: julianporter
'''

from .direction import Direction

NAME_KEY   = 'name'
INPUT_KEY  = 'max_input_channels'
OUTPUT_KEY = 'max_output_channels'
SAMPLE_KEY = 'default_samplerate'

class Dev(object):
    
    NAME_KEY   = 'name'
    INPUTS_KEY  = 'max_input_channels'
    OUTPUTS_KEY = 'max_output_channels'
    SAMPLE_KEY = 'default_samplerate'
    
    def __init__(self,d={},index=0):
        self._dict=d
        self.index=index
    
    def __getitem__(self,key):
        if key == Direction.input: return self._dict[self.INPUTS_KEY]
        elif key == Direction.output: return self._dict[self.OUTPUTS_KEY]
        else: return self._dict[key]  
    
    @property
    def name(self): return self[self.NAME_KEY]
    @property
    def maxIn(self): return self[Direction.input]
    @property
    def maxOut(self): return self[Direction.output]
    @property
    def rate(self): return self[self.SAMPLE_KEY]
    
    def hasDirection(self,direction): return self[direction]>0
    def nChannels(self,direction): return self[direction]
    
    @property
    def totalChannels(self):
        return self.maxIn + self.maxOut
      
    

class PCMDeviceSpecification(object):
    
    def __init__(self,direction: Direction = Direction.input,device = Dev()):
        self._dev=device
        self.direction = direction
        self.card=self._dev.name
        self.name=self._dev.name
        self.index=self._dev.index
        #self.channel = channel
        self.rate = self._dev.rate
        
    def __getitem__(self,key):
        return self._dev[key]
    
    #def __str__(self): return f'{self.card} channel {self.channel}'
    def __str__(self): return f'{self.card}'
    
        