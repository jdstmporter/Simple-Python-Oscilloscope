'''
Created on 4 Mar 2020

@author: julianporter
'''

import enum
import alsaaudio

class Direction(enum.Enum):
    input = alsaaudio.PCM_CAPTURE
    output = alsaaudio.PCM_PLAYBACK
    
    @classmethod
    def all(cls):
        return [x for x in cls.__members__.values()]