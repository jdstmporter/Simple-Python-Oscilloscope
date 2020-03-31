'''
Created on 4 Mar 2020

@author: julianporter
'''

import alsaaudio
from .device import PCMDeviceSpecification
import multiprocessing



def runner(pcm,flag,queue):
    while flag.value == 1:
        n, data = pcm.read()
        if n>0:
            values = [int.from_bytes(data[2*i:2*(i+1)], byteorder='little', signed=True) for i in range(n)]
            try:
                queue.put_nowait(values)
            except:
                pass
            

class PCMSession(object):
    
    def __init__(self,specification : PCMDeviceSpecification):
        self.device=str(specification)
        self.name=specification.name
        self.direction=specification.direction
        self.pcm=None
        self.active=None
        self.queue=multiprocessing.Queue()
        
        # need to put in a queue here, because, as it is, we never get off the ALSA thread
        
    def connect(self,pcmFormat = alsaaudio.PCM_FORMAT_S16_LE, rate = 48000,blocksize=64):
        self.pcm=alsaaudio.PCM(type=self.direction.value, mode=alsaaudio.PCM_NORMAL, device=self.name)
        self.pcm.setrate(rate)
        self.pcm.setformat(pcmFormat)
        self.pcm.setchannels(1)
        self.pcm.setperiodsize(blocksize)
        
        self.active = multiprocessing.Value('i',1)
        p = multiprocessing.Process(target=runner,args=(self.pcm,self.active,self.queue))
        p.start()
        return p
            
    def stop(self):
        if self.active:
            self.active.value=0
        if self.pcm:
            self.pcm.close()
        self.pcm=None
        
    def hasData(self):
        return not self.queue.empty()
    
    def readSync(self):
        return self.queue.get()
     
    def readAsync(self):
        try:
            return self.queue.get_nowait()
        except:
            return None
        
        

            
        
    
        