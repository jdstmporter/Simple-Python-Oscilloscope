'''
Created on 1 Apr 2020

@author: julianporter
'''
import numpy as np


        
class PCMData(object):
    
    def __init__(self,timestamp=None,data=np.array([])): 
        self.data=data[:]
        self.timestamp=timestamp
        
    @property
    def nChannels(self):
        return self.data.shape[1]
        
    def __call__(self):
        return np.mean(self.data,axis=1)
        
    def __getitem__(self,n):
        return self.data[:,n]
    
    def __len__(self):
        return self.data.shape[0]
    
    @property
    def mean(self):
        return np.mean(self())       
