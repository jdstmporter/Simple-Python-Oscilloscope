#!/usr/bin/env python3

'''
Created on 3 Mar 2020

@author: julianporter
'''

import tkinter as tk
import tkinter.ttk as ttk
from collections import OrderedDict
import math
import numpy as np
from portaudio import PCMSystem, PCMSession, PCMSessionDelegate
from graphs import GraphView, Graph, SpectralView, VUMeter
from util import SYSLOG, Range


def safe(action):
    try:
        action()
    except Exception as ex:
        SYSLOG.debug(f'Ignored {ex}')

class App(PCMSessionDelegate):

    BUFFER_LENGTH = 64
    DB_OFFSET = -10.0*math.log10(32768.0)

    def __init__(self):
        self.root = tk.Tk()
        self.root.protocol('WM_DELETE_WINDOW', self.shutdown)

        self.content = ttk.Frame(self.root, width=300, height=500)
        self.content.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.root.columnconfigure(0, weight=5)
        self.root.columnconfigure(4, weight=1)
        self.root.rowconfigure(0, weight=1)

        pcm = PCMSystem()
        self.devices = OrderedDict()
        for dev in pcm.inputs():
            self.devices[dev.name] = dev
            SYSLOG.debug(f'Device : {dev.name} {dev.maxIn} {dev.rate}')
        self.currentDevice = tk.StringVar()
        self.currentDevice.set(self[0].name)

        self.cards = ttk.Combobox(self.content, textvariable=self.currentDevice,
                                  values=self.names, justify=tk.LEFT)
        self.cards.bind('<<ComboboxSelected>>', self.changeCard)
        self.cards.grid(column=0, row=0, columnspan=5, sticky=(tk.N, tk.S, tk.E, tk.W))

        #self.graph = Graph(self.content, bounds=Range(-40, 10))
        #self.graph.grid(column=0, row=1, columnspan=4, sticky=(tk.N, tk.S, tk.E, tk.W))
        #self.graph.bind('<Button-1>', self.onClick)
        
        self.graphs = GraphView(self.content,bounds=Range(-40, 0))
        self.graph=self.graphs.addViewer(Graph)
        self.graph.grid(column=0, row=1, columnspan=4, sticky=(tk.N, tk.S, tk.E, tk.W))
        #self.graph.bind('<Button-1>', self.onClick)
        
        self.vu = self.graphs.addViewer(VUMeter)
        self.vu.configure(width=80)
        self.vu.grid(column=4, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        

        self.spec = tk.Toplevel(self.root, width=800, height=500)
        self.fft = SpectralView(self.spec, bounds=Range(-80, 40), fftSize=1024)
        self.fft.configure(width=800, height=500)
        self.fft.pack()
        
        self.startButton = ttk.Button(self.content, text='Start', command=self.start)
        self.stopButton = ttk.Button(self.content, text='Stop', command=self.stop)
        self.clearButton = ttk.Button(self.content, text='Clear', command=self.graph.clear)

        self.clearButton.grid(column=0, row=2, sticky=(tk.N, tk.S, tk.W))
        self.startButton.grid(column=3, row=2, sticky=(tk.N, tk.S, tk.E))
        self.stopButton.grid(column=4, row=2, sticky=(tk.N, tk.S, tk.E, tk.W))

        for column in [0, 3, 4]:
            self.content.columnconfigure(column, weight=1)
        self.content.rowconfigure(1, weight=1)

        self.timer = None
        self.samples = []
        self.session = PCMSession(self[0], delegate=self)
        self.format = None

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
            if dev == self.session.pcm:
                return
            SYSLOG.info(f'Changing to {dev}')
            self.stop()
            self.session = PCMSession(dev, delegate=self)
            self.graphs.setSampleRate(self.session.samplerate)
            self.start()
        except Exception as ex:
            SYSLOG.error(f'{event} - {ex}')

    def __call__(self, data):
        if len(data) > 0:
            #data=self.format(data)
            #self.samples.append(data)
            
            self.graphs.add(data)
            self.fft.add(data)
            
            
            


    def start(self):
        self.stop()     # make sure we're in a known state
        #self.timer = MultiTimer(interval=0.05, function=self.update, runonstart=False)
        #self.timer.start()
        #self.spectrogram.start()
        self.fft.start()
        self.graphs.start()
        self.session.start()
        self.format = self.session.format
        SYSLOG.info(f'Started {self.session}')

    def stop(self):
        if self.session:
            self.session.stop()
            self.format=None
        #if self.timer:
        #   self.timer.stop()
        if self.fft:
            self.fft.stop()
        if self.graphs:
            self.graphs.stop()
        #if self.spectrogram: self.spectrogram.stop()
        self.timer = None

    def shutdown(self):
        self.stop()
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
