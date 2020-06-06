'''
Created on 6 Jun 2020

@author: julianporter
'''
import jack
import numpy
  
      

class JackClient(object):
    
    def __init__(self,name,inports=[],outports=[]):
        self.name=name
        self.client=jack.Client(self.name)
        
        self.allPorts=[]
        self.inports = dict()
        for port in inports:
            p=self.client.inports.register(port)
            self.allPorts.append(p)
            self.inports[port]=p
        self.outports = dict()
        for port in outports:
            p=self.client.outports.register(port)
            self.allPorts.append(p)
            self.outports[port]=p
            
        
            
        self.active=False
        self.blockSize=64
        self.sampleRate=41000
        
        self.client.set_shutdown_callback(self._shutdown)
        self.client.set_blocksize_callback(self._blocksize)
        self.client.set_samplerate_callback(self._rate)
        self.client.set_process_callback(self.process)
        
    def _shutdown(self,status,reason):
        print(f'Shutdown with status {status} and reason {reason}')
        self.active=False
        
    def _blocksize(self,blocksize):
        print(f'Setting blocksize to {blocksize}')
        self.blockSize=blocksize
        
    def _rate(self,rate):
        print(f'Setting sample rate to {rate}')
        self.sampleRate=rate

    def process(self,frames):
        pass
    
    def connect(self,**ports):
        pass
        '''
        for fr, to in ports.items():
            try:
                print(f'Connecting {fr} -> {to}')
                self.client.connect(to,fr)
            except jack.JackError as e:
                print(f'JACK Error: {e}')
        '''
            
    def disconnect(self):
        for port in self.allPorts:
            port.disconnect()
            
    def start(self):
        self.client.activate()
        self.sampleRate=self.client.samplerate
        
    def stop(self):
        self.active=False
        self.client.deactivate()
    
    def shutdown(self):
        self.client.close()
            
            
    def read(self,name):
        return self.inports[name].get_array()
    
    def write(self,name,data):
        self.outports[name].get_array()[:]=data
    
    def __enum__(self):
        return enumerate(self.client.get_ports())
    
    