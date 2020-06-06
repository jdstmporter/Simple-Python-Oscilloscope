'''
Created on 6 Jun 2020

@author: julianporter
'''
from .client import JackClient
import numpy
from util import SYSLOG

class JackSessionDelegate(object):
    
    def __call__(self,data):
        pass
    
    def connect(self,samplerate):
        pass
    
    def startListeners(self):
        pass
    
    def stopListeners(self):
        pass

class JackSessionHandler(object):
    def __init__(self,delegate=JackSessionDelegate()):
        self.pcm=None
        self.format=None
        self.delegate=delegate
        
        
    def connect(self,**connections):
        try:
            SYSLOG.info('Initialising connection to JACK')
            if self.pcm:
                SYSLOG.info('Stopping session')
                self.stop()
            else:
                SYSLOG.info('Initialising session')
                self.pcm=JackSession('fred',callback=self.delegate)
                SYSLOG.info('Initialised')
            SYSLOG.info(f'Connecting {connections}')
            self.pcm.connect(**connections)
            SYSLOG.info('Connecting delegate')
            self.delegate.connect(self.pcm.sampleRate)  
            SYSLOG.info('Connected to JACK')        
        except Exception as ex:
            SYSLOG.error(f'Error connecting to {connections} : {ex}')
            
    def disconnect(self):
        try:
            if self.pcm:
                self.stop()
                self.pcm.shutdown()
                self.pcm=None
        except Exception as ex:
            SYSLOG.error(f'Error disconnecting from {self.pcm} : {ex}')
            
    def start(self):
        self.delegate.startListeners()
        self.pcm.start()
        self.format='float32'
        SYSLOG.info(f'Started {self.pcm}')
        
        
    def stop(self):
        if self.pcm:
            self.pcm.stop()
            self.pcm.disconnect()
            self.format=None
        self.delegate.stopListeners()
    
  

class JackSession(JackClient):
    
    def __init__(self,name,callback):
        super().__init__(name,inports=['thru_in'],outports=['thru_out'])
        self.callback=callback
        
    def process(self, frames):
        if frames>0:
            newData = self.read('thru_in')
            self.callback(newData)
        self.write('thru_out',newData)
        
        
                
        
        
        
                
        