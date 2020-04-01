'''
Created on 1 Apr 2020

@author: julianporter
'''

import enum

class Direction(enum.Enum):
    input = 'I'
    output = 'O'
    
    @classmethod
    def all(cls):
        return [x for x in cls.__members__.values()]