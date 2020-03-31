'''
Created on 3 Mar 2020

@author: julianporter
'''

import re
from typing import Mapping
from .direction import Direction

class PCMDeviceSpecification(object):
    
    format = '([a-z0-9]+):CARD=([A-Za-z0-9]+)(?:,DEV=([0-9]+)){0,1}'
    
    def __init__(self,cards : Mapping[str,int], string : str, direction: Direction):
        matcher = re.match(self.format,string)
        self._string=string
        if matcher:
            self._prefix = matcher.group(1)
            self._card = matcher.group(2)
            self._index = cards.get(self._card)
            self._subindex = None if not matcher.group(3) else int(matcher.group(3)) 
        else:
            self._prefix = None
            self._card = None
            self._index = None
            self._subindex = None
            
        self._direction = direction
    
    def __str__(self):
        return self._string
    
    @property
    def prefix(self): return self._prefix
    
    @property
    def card(self): return self._card
    
    @property
    def index(self): return self._index
    
    @property
    def subindex(self): return self._subindex
    
    @property
    def direction(self): return self._direction
    
    @property 
    def name(self): return self._string
    
    
            
            
    def __str__(self):
        parts=[]
        if self.prefix:
            parts.append(f'{self.prefix}:')
            parts.append(f'{self.card}' if self.index is None else f'{self.index}')
            if self.subindex is not None:
                parts.append(f',{self.subindex}')
        else:
            parts.append(f'{self.name}')
        return ''.join(parts)
    

        
    