'''
Created on 13 Jun 2020

@author: julianporter
'''
from collections import defaultdict
from util import SYSLOG

class ConfigurableMeta(type):
    def __new__(cls,name,bases,attrs):
        c=super().__new__(cls,name,bases,attrs)
        if not hasattr(c,'_registry'):
            c._registry=defaultdict(lambda : [])
        return c
            
    def __call__(cls,*args,**kwargs):
        obj=super().__call__(*args,**kwargs)
        cls._registry[cls.__name__].append(obj)
        return obj
    
class RootConfigurable(metaclass=ConfigurableMeta):
    
    @classmethod
    def instances(cls):
        return cls._registry[cls.__name__]
        
class RangePickerDelegate(RootConfigurable):
    
    def __call__(self,bounds):
            SYSLOG.debug(f'Range is now {bounds}')
            
class GradientPickerDelegate(RootConfigurable):
    
    def __call__(self,gradient):
            SYSLOG.debug(f'Gradient is now {gradient}')
        
class AlgorithmPickerDelegate(RootConfigurable):
    
    def __call__(self,algorithm):
            SYSLOG.debug(f'Changing algorithm to {algorithm}')
            
class DelegateMixin:
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
    def __call__(self,*args,**kwargs):
        pass
    
   
class ListenerMixin:
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.listeners=[]
        
    def addListeners(self,*args):
        self.listeners.extend(args)
        
    def callListeners(self,*args,**kwargs):
        for delegate in self.listeners:
            delegate(*args,**kwargs)
        
        