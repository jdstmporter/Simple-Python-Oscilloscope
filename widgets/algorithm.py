'''
Created on 20 Jul 2020

@author: julianporter
'''

import tkinter as tk
import tkinter.ttk as ttk
from enum import Enum
from util import SYSLOG
from .configurable import DelegateMixin, ListenerMixin

class SimpleAlgorithmDelegate(DelegateMixin,object):
    
    def __init__(self):
        super().__init__()
        
    def __call__(self,value):
        SYSLOG.info(f'Changed algorithm to {value}')

class AlgorithmPicker(ListenerMixin,ttk.LabelFrame):
    
    class Algorithm(Enum):
        FFT = 1
        Harmonic = 2
        Cepstrum = 3
        Corr = 4
    
    Algorithms = [('Power spectrum', Algorithm.FFT),
                  ('Harmonic spectrum', Algorithm.Harmonic),
                  ('Cepstrum', Algorithm.Cepstrum), 
                  ('Autocorrelation', Algorithm.Corr)]
    
    def __init__(self,root,name='Algorithm'):
        super().__init__(root,text=name)
        
        
        self.current=tk.StringVar()
        self.current.set(self.Algorithms[0][0]) 
        self.currentAlg = None
        self.names=[x[0] for x in self.Algorithms]       
        self.picker = ttk.Combobox(self, textvariable=self.current,values=self.names, justify=tk.LEFT)
        self.picker.bind('<<ComboboxSelected>>', self.changeAlgorithm)
        self.picker.grid(column=0,row=0,sticky=(tk.E,tk.W))
        
    def algorithm(self):
        s = self.current.get()
        return [y for (x,y) in self.Algorithms if x==s][0]

        
        
    def changeAlgorithm(self,event=None):
        try:
            alg=self.algorithm()
            if alg is not self.currentAlg:
                self.currentAlg=alg
                self.callListeners(alg)
        except:
            SYSLOG.error('Unexpected algorithm selection') 
