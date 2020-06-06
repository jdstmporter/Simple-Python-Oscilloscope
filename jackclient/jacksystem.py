'''
Created on 6 Jun 2020

@author: julianporter
'''
from .client import JackClient


class JackSystem(JackClient):
    
    def __init__(self):
        super().__init__(name='probe')
        self.start()
        
    def writeable(self):
        devs=self.client.get_ports(is_audio=True,is_input=True)
        return [dev.name for dev in devs]
        
    
    def readable(self):
        devs=self.client.get_ports(is_audio=True,is_output=True)
        return [dev.name for dev in devs]
        
    