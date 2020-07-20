'''
Created on 8 Jun 2020

@author: julianporter
'''
import tkinter as tk
import tkinter.ttk as ttk
from enum import Enum
from util import SYSLOG, Range
from .configurable import RangePickerDelegate

  
    


class RangePicker(ttk.LabelFrame):
    
    class Child(Enum):
        MAX=1
        MIN=2
    
    def __init__(self,root,name='Range',bounds=Range(-1,1),initial=Range(0,0),
                 delegate=RangePickerDelegate()):
        super().__init__(root,text=name) # borderwidth=2,relief=tk.GROOVE)
        
        self.delegate=delegate
        self.lower, self.upper = bounds.bounds()
        self.min, self.max = initial.bounds()
        
        
        self.name=name
        validate=self.register(self.valueChanged)
        invalid=self.register(self.invalidValue)
        
        self._min=tk.StringVar()
        self._min.set(str(self.min))
        
        minLabel=ttk.Label(self,justify=tk.LEFT,text='Min',padding='1m')
        self.minText=ttk.Entry(self,justify=tk.LEFT,textvariable=self._min,
                               validate='focusout',validatecommand=(validate,'%W', '%P'),
                               invalidcommand=(invalid,'%W'))
        
        
        
        self._max=tk.StringVar()
        self._max.set(str(self.max))
        maxLabel=ttk.Label(self,justify=tk.LEFT,text='Max',padding='1m')
        self.maxText=ttk.Entry(self,justify=tk.LEFT,textvariable=self._max,
                               validate='focusout',validatecommand=(validate,'%W','%P'),
                               invalidcommand=(invalid,'%W'))
        
        minLabel.grid(column=0,row=0,sticky=(tk.E,tk.W))
        self.minText.grid(column=1,row=0,sticky=(tk.E,tk.W))
        maxLabel.grid(column=2,row=0,sticky=(tk.E,tk.W))
        self.maxText.grid(column=3,row=0,sticky=(tk.E))
        
        self.parts = {
            str(self.minText) : RangePicker.Child.MIN,
            str(self.maxText) : RangePicker.Child.MAX,
        }
        self.vars = {
            RangePicker.Child.MIN : self._min,
            RangePicker.Child.MAX : self._max
        }
    
    def range(self):
        return Range(self.min,self.max)
    
    
    
    def valueChanged(self,name,newValue):
        try:
            which = self.parts[name]
            print(f'Validation on {name} : {which} {newValue}')
            value = float(newValue)
            if value<self.lower or value>self.upper:
                raise Exception('out of allowed range')
            if which==RangePicker.Child.MIN:
                if value>self.max:
                    raise Exception('new min above max')
                elif value != self.min:
                    self.min=value
                    self.delegate.setRange(self.range())
            elif which==RangePicker.Child.MAX:
                if value<self.min:
                    raise Exception('new max below min')
                elif value != self.max:
                    self.max=value
                    self.delegate.setRange(self.range())
            return True
        except Exception as e:
            SYSLOG.info(f'Range value rejected because: {e}')
            return False
    
    def invalidValue(self,name):
        try:
            which = self.parts[name]
            print(f'Correction on {name} : {which}')
            if which==RangePicker.Child.MIN:
                self._min.set(str(self.min))
            elif which==RangePicker.Child.MAX:
                self._max.set(str(self.max))
        except:
            pass
        
        