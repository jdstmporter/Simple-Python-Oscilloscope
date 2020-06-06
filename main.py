#!/usr/bin/env python3

'''
Created on 3 Mar 2020

@author: julianporter
'''

import tkinter as tk
import tkinter.ttk as ttk
from jackclient import JackSystem, JackSessionHandler, JackSessionDelegate
from graphs import GraphView, Graph, SpectralView, VUMeter, Stick
from util import SYSLOG, Range
from graphs.spectra.spectrogram import Spectrogram
from graphs.spectra.spectrum import SpectrumView


def safe(action):
    try:
        action()
    except Exception as ex:
        SYSLOG.debug(f'Ignored {ex}')

class App(object):
    
    class Delegate(JackSessionDelegate):
        
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
        self.system=JackSystem()
        
        '''
        Row 0: the sound card selector
        '''
        self.devices=self.system.readable()
        for name in self.devices:
            SYSLOG.debug(f'Device : {name}')
        self.currentDevice = tk.StringVar()
        self.currentDevice.set(self.devices[0])

        self.cards = ttk.Combobox(self.root, textvariable=self.currentDevice,
                                  values=self.devices, justify=tk.LEFT)
        self.cards.bind('<<ComboboxSelected>>', self.changeCard)
        self.cards.grid(column=0, row=0, columnspan=2,sticky=Stick.ALL)

        '''
        Row 1 : the spectral view, made up of the spectrogram and the spectral graph
        '''
        self.fft = SpectralView(self.root, bounds=Range(-50, 40), fftSize=1024)
        
        self.spectrogram = self.fft.addViewer(Spectrogram)
        self.spectrogram.grid(row=1,column=0,sticky=Stick.ALL)
        self.spectrogram.scroll.grid(row=2,column=0,sticky=Stick.ALL)
        self.spectrum = self.fft.addViewer(SpectrumView)
        self.spectrum.grid(column=1, row=1, sticky=Stick.ALL)
        
        self.spectrogram.configure(width=800, height=300)
        self.spectrum.configure(width=200,height=300)
        
        
        '''
        Row 2 : the averaged amplitude display, made up of the graph and the VU meter 
        '''
        
        self.lower = ttk.Frame(self.root)
         
        self.graphs = GraphView(self.root,bounds=Range(-40, 0))
        self.graph=self.graphs.addViewer(Graph)
        self.graph.grid(row=3,column=0, sticky=Stick.ALL)
        self.vu = self.graphs.addViewer(VUMeter)
        self.vu.grid(row=3,column=1, sticky=Stick.ALL,padx=0,pady=0)
        self.vu.configure(width=200,height=300)
        self.graph.configure(width=800, height=300)
        self.lower.columnconfigure(1,weight=1,pad=0)
        
        '''
        Row 3 : the global control buttons
        '''
        
        self.controls = ttk.Frame(self.root)
        self.controls.grid(row=4,column=0,columnspan=2,sticky=Stick.ALL)
   
        self.startButton = ttk.Button(self.controls, text='Start', command=self.start)
        self.stopButton = ttk.Button(self.controls, text='Stop', command=self.stop)
        self.clearButton = ttk.Button(self.controls, text='Clear', command=self.graph.clear)
        self.clearButton.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.W))
        self.startButton.grid(column=2, row=0, sticky=(tk.N, tk.S, tk.E))
        self.stopButton.grid(column=3, row=0, sticky=(tk.N, tk.S))
        
        self.controls.columnconfigure(1,weight=5)
        
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=0)
        
        
        '''
        Setting up the session to connect to the audio subsystem
        '''
        
        delegate = App.Delegate([self.fft,self.graphs])
        self.session = JackSessionHandler(delegate=delegate)
        self.session.connect(thru_in=self.devices[0])

    def onClick(self, event):
        SYSLOG.debug(f'Click on {event.widget}')
        canvas = event.widget
        xPos = canvas.canvasx(event.x)
        yPos = canvas.canvasy(event.y)
        print(f'{self.graph.size} : ({event.x},{event.y}) -> ({xPos},{yPos})')

    

    def __getitem__(self, index):
        if isinstance(index, str):
            return index
        return self.devices[index]

    def changeCard(self, event=None):
        try:
            if self.session is None:
                return
            dev = self.currentDevice.get()
            SYSLOG.info(f'Changing to {dev}')
            self.session.stop()
            self.session.connect(thru_in=dev)
            self.session.start()
        except Exception as ex:
            SYSLOG.error(f'Error changing card: {event} - {ex}')
    
    
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
