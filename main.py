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


def safe(action):
    try:
        action()
    except Exception as ex:
        SYSLOG.debug(f'Ignored {ex}')

class App(PCMSessionDelegate):

    BUFFER_LENGTH = 64


    def __init__(self):
        self.root = tk.Tk()
        self.root.protocol('WM_DELETE_WINDOW', self.shutdown)

        self.content = ttk.Frame(self.root, width=300, height=500)
        self.content.grid(column=0, row=0, sticky=Stick.ALL)

        self.root.columnconfigure(0, weight=5)
        self.root.columnconfigure(4, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.devices=PCMSystem.devices()
        for name, dev in self.devices.items():
            SYSLOG.debug(f'Device : {name} {dev.maxIn} {dev.rate}')
        self.currentDevice = tk.StringVar()
        self.currentDevice.set(self[0].name)

        self.cards = ttk.Combobox(self.content, textvariable=self.currentDevice,
                                  values=self.names, justify=tk.LEFT)
        self.cards.bind('<<ComboboxSelected>>', self.changeCard)
        self.cards.grid(column=0, row=0, columnspan=5, sticky=Stick.ALL)

        self.graphs = GraphView(self.content,bounds=Range(-40, 0))
        self.graph=self.graphs.addViewer(Graph)
        self.graph.grid(column=0, row=1, columnspan=4, sticky=Stick.ALL)
        
        self.vu = self.graphs.addViewer(VUMeter)
        self.vu.configure(width=80)
        self.vu.grid(column=4, row=1, sticky=Stick.ALL)
        
        self.spec = tk.Toplevel(self.root, width=800, height=500)
        self.fft = SpectralView(self.spec, bounds=Range(-50, 40), fftSize=1024)
        
        self.spectrogram = self.fft.addViewer(Spectrogram)
        self.spectrogram.grid(column=0, row=0, sticky=Stick.ALL)
        self.spectrogram.scroll.grid(column=0,row=1, sticky=Stick.ALL)
        
        self.spectrum = self.fft.addViewer(SpectrumView)
        self.spectrum.grid(column=0, row=2, sticky=Stick.ALL)
        
        self.fft.configure(width=800, height=500)
        self.fft.pack()
        
        self.startButton = ttk.Button(self.content, text='Start', command=self.start)
        self.stopButton = ttk.Button(self.content, text='Stop', command=self.stop)
        self.clearButton = ttk.Button(self.content, text='Clear', command=self.graph.clear)

        self.clearButton.grid(column=0, row=2, sticky=(tk.N, tk.S, tk.W))
        self.startButton.grid(column=3, row=2, sticky=(tk.N, tk.S, tk.E))
        self.stopButton.grid(column=4, row=2, sticky=Stick.ALL)

        for column in [0, 3, 4]:
            self.content.columnconfigure(column, weight=1)
        self.content.rowconfigure(1, weight=1)

        self.session = PCMSessionHandler(delegate=self)
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
    
    def connect(self,samplerate):
        self.graphs.setSampleRate(samplerate) 
    
    def startListeners(self):
        self.graphs.start()
        self.fft.start()
        
    def stopListeners(self):
        self.fft.stop()
        self.graphs.stop()                
                          
    def __call__(self, data):
        if len(data) > 0:
            self.fft.add(data)
            self.graphs.add(data)      


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
