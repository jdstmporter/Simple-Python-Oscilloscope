#!/usr/bin/env python3

'''
Created on 3 Mar 2020

@author: julianporter
'''

import tkinter as tk
import tkinter.ttk as ttk
from portaudio import PCMSystem, PCMSessionHandler, PCMSessionDelegate
from graphs import GraphView, Graph, SpectralView, VUMeter, Stick
from util import SYSLOG, Range
from graphs.spectra.spectrogram import Spectrogram
from graphs.spectra.spectrum import SpectrumView
from enum import Enum

def safe(action):
    try:
        action()
    except Exception as ex:
        SYSLOG.debug(f'Ignored {ex}')
        
        
class RangePicker(ttk.LabelFrame):
    class Child(Enum):
        MAX=1
        MIN=2
    
    def __init__(self,root,name='Range',bounds=Range(-1,1),initial=Range(0,0),
                 callback=lambda x : x):
        super().__init__(root,text=name) # borderwidth=2,relief=tk.GROOVE)
        
        self.callback=callback
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
        
    def __getitem__(self,part):
        if part==RangePicker.Child.MIN:
            return self.min
        else:
            return self.max
        
    def __setitem__(self,part,value):
        if part==RangePicker.Child.MIN:
            self.min=value
        else:
            self.max=value
        
    
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
                    self.callback(self.range())
            elif which==RangePicker.Child.MAX:
                if value<self.min:
                    raise Exception('new max below min')
                elif value != self.max:
                    self.max=value
                    self.callback(self.range())
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
        
        
        
class Tabs(Enum):
    FFT = 1
    SAMPLES = 2
    

class App(object):
    
    class Delegate(PCMSessionDelegate):
        
        def __init__(self,listeners=[]):
            super().__init__()
            self.listeners=listeners
            
        def connect(self,samplerate):
            for listener in self.listeners:
                if hasattr(listener,'setSampleRate'):
                    listener.setSampleRate(samplerate)
                    
        def startListeners(self):
            for listener in self.listeners:
                listener.start()
                
        def stopListeners(self):
            for listener in self.listeners:
                listener.stop()
                
        def __call__(self,data):
            if len(data) > 0:
                for listener in self.listeners:
                    listener.add(data)
            
    BUFFER_LENGTH = 64


    def __init__(self):
        self.root = tk.Tk()
        self.root.protocol('WM_DELETE_WINDOW', self.shutdown)
        
        
        '''
        Row 0: the sound card selector
        '''
        self.devices=PCMSystem.devices()
        for name, dev in self.devices.items():
            SYSLOG.debug(f'Device : {name} {dev.maxIn} {dev.rate}')
        self.currentDevice = tk.StringVar()
        self.currentDevice.set(self[0].name)

        self.cards = ttk.Combobox(self.root, textvariable=self.currentDevice,
                                  values=self.names, justify=tk.LEFT)
        self.cards.bind('<<ComboboxSelected>>', self.changeCard)
        self.cards.grid(column=0, row=0, columnspan=2,sticky=Stick.ALL)

        self.notebook = ttk.Notebook(self.root)
        self.first = tk.Frame()
        
        '''
        Row 1 : the spectral view, made up of the spectrogram and the spectral graph
        '''
        self.fft = SpectralView(self.first, bounds=Range(-50, 40), fftSize=1024)
        
        self.spectrogram = self.fft.addViewer(Spectrogram)
        self.spectrogram.grid(row=0,column=0,sticky=Stick.ALL)
        self.spectrogram.scroll.grid(row=1,column=0,sticky=Stick.ALL)
        self.spectrum = self.fft.addViewer(SpectrumView)
        self.spectrum.grid(column=1, row=0, sticky=Stick.ALL)
        
        self.spectrogram.configure(width=800, height=300)
        self.spectrum.configure(width=200,height=300)
        
        
        self.notebook.add(self.first,text='FFT')
        
        '''
        Row 2 : the averaged amplitude display, made up of the graph and the VU meter 
        '''
        
        self.second = ttk.Frame()
         
        self.graphs = GraphView(self.second,bounds=Range(-40, 0))
        self.graph=self.graphs.addViewer(Graph)
        self.graph.grid(row=0,column=0, sticky=Stick.ALL)
        self.vu = self.graphs.addViewer(VUMeter)
        self.vu.grid(row=0,column=1, sticky=Stick.ALL,padx=0,pady=0)
        self.vu.configure(width=200,height=300)
        self.graph.configure(width=800, height=300)
        self.second.columnconfigure(1,weight=1,pad=0)
        
        self.notebook.add(self.second,text='Samples')
        
        self.notebook.select(self.first)
        self.notebook.grid(row=1,column=0,sticky=Stick.ALL)
        self.notebook.bind('<<NotebookTabChanged>>', self.changeTab)
        
        self.tabs = {
            str(self.first) : Tabs.FFT,
            str(self.second) : Tabs.SAMPLES
            }
        self.actors = {
            Tabs.FFT : self.fft,
            Tabs.SAMPLES : self.graphs
        }
                
        '''
        Row 3 : the global control buttons
        '''
        
        self.controls = ttk.Frame(self.root)
        self.controls.grid(row=2,column=0,sticky=Stick.ALL)
   
        self.startButton = ttk.Button(self.controls, text='Start', command=self.start)
        self.stopButton = ttk.Button(self.controls, text='Stop', command=self.stop)
        self.clearButton = ttk.Button(self.controls, text='Clear', command=self.graph.clear)
        self.clearButton.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.W))
        self.startButton.grid(column=2, row=0, sticky=(tk.N, tk.S, tk.E))
        self.stopButton.grid(column=3, row=0, sticky=(tk.N, tk.S))
        
        self.controls.columnconfigure(1,weight=5)
        
        self.maxmin = RangePicker(self.root)
        self.maxmin.grid(row=3,column=0,sticky=Stick.ALL)
        
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=0)
        
        
        '''
        Setting up the session to connect to the audio subsystem
        '''
        
        delegate = App.Delegate([self.fft,self.graphs])
        self.session = PCMSessionHandler(delegate=delegate)
        self.session.connect(self[0])

    def onClick(self, event):
        SYSLOG.debug(f'Click on {event.widget}')
        canvas = event.widget
        xPos = canvas.canvasx(event.x)
        yPos = canvas.canvasy(event.y)
        print(f'{self.graph.size} : ({event.x},{event.y}) -> ({xPos},{yPos})')

    @property
    def names(self):
        return list(self.devices.keys())

    def __getitem__(self, index):
        if isinstance(index, str):
            return self.devices[index]
        return self.devices[self.names[index]]

    def changeCard(self, event=None):
        try:
            if self.session is None:
                return
            dev = self[self.currentDevice.get()]
            if dev == self.session.pcm.pcm:
                return
            SYSLOG.info(f'Changing to {dev}')
            self.session.stop()
            self.session.connect(dev)
            self.session.start()
        except Exception as ex:
            SYSLOG.error(f'Error changing card: {event} - {ex}')
    
    def changeTab(self,event=None):
        try:
            wName = self.notebook.select()
            tab = self.tabs[wName]
            for k, v in self.actors.items():
                v.activate(k==tab)
            SYSLOG.info(f'Switched to {wName} - {tab}')
        except Exception as ex:
            SYSLOG.error(f'Error changing tab: {event} - {ex}')
    
    def start(self):
        self.session.stop()     # make sure we're in a known state
        self.session.start()
        SYSLOG.info(f'Started {self.session}')

    def stop(self):
        if self.session:
            self.session.stop()

    def shutdown(self):
        self.session.disconnect()
        self.root.destroy()

    def run(self):
        try:
            self.start()
            self.root.mainloop()
        except Exception as ex:
            SYSLOG.error(f'Mainloop stopped with {ex}')
        finally:
            self.stop()


if __name__ == '__main__':
    app = App()
    app.run()
