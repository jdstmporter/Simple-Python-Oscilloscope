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
from multitimer import MultiTimer
from portaudio import PCMSystem, PCMSession, PCMSessionDelegate
from graphs import GraphView, SpectralView
from util import SYSLOG, Range, RedGreenBlueGradient


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

        self.root.columnconfigure(0, weight=1)
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
        self.cards.grid(column=0, row=0, columnspan=4, sticky=(tk.N, tk.S, tk.E, tk.W))

        #self.graph = Graph(self.content, bounds=Range(-40, 10))
        #self.graph.grid(column=0, row=1, columnspan=4, sticky=(tk.N, tk.S, tk.E, tk.W))
        #self.graph.bind('<Button-1>', self.onClick)
        
        self.graph = GraphView(self.content, bounds=Range(-40, 10))
        self.graph.grid(column=0, row=1, columnspan=4, sticky=(tk.N, tk.S, tk.E, tk.W))
        #self.graph.bind('<Button-1>', self.onClick)

        gradient = RedGreenBlueGradient
        self.spec = tk.Toplevel(self.root, width=800, height=500)
        self.fft = SpectralView(self.spec, bounds=Range(-50, 40), gradient=gradient, fftSize=1024)
        self.fft.configure(width=800, height=500)
        self.fft.pack()
        #self.spectrum=SpectrumView(self.spec,bounds=Range(-50,40),xflen=513)
        #self.spectrum.configure(width=800,height=300)
        #self.spectrum.pack()
        #self.spectro = tk.Toplevel(self.root,width=800,height=400)
        #self.spectrogram=Spectrogram(self.spectro,bounds=Range(-40,50),gradient=gradient,xflen=513)
        #self.spectrogram.configure(width=800,height=400)
        #self.spectrogram.pack()
        #self.fft = SpectralBase(fftSize=1024,viewers=[self.spectrum,self.spectrogram])
        self.startButton = ttk.Button(self.content, text='Start', command=self.start)
        self.stopButton = ttk.Button(self.content, text='Stop', command=self.stop)
        self.clearButton = ttk.Button(self.content, text='Clear', command=self.graph.clear)

        self.clearButton.grid(column=0, row=2, sticky=(tk.N, tk.S, tk.W))
        self.startButton.grid(column=2, row=2, sticky=(tk.N, tk.S, tk.E))
        self.stopButton.grid(column=3, row=2, sticky=(tk.N, tk.S, tk.E, tk.W))

        for column in [0, 2, 3]:
            self.content.columnconfigure(column, weight=1)
        self.content.rowconfigure(1, weight=1)

        self.timer = None
        self.samples = []
        self.session = PCMSession(self[0], delegate=self)

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
            self.fft.setSampleRate(self.session.samplerate)
            self.graph.setSampleRate(self.session.samplerate)
            self.start()
        except Exception as ex:
            SYSLOG.error(f'{event} - {ex}')

    def __call__(self, data):
        if len(data) > 0:
            #self.samples.append(data)
            self.fft.add(data)
            self.graph.add(data)
            

    def update(self):
        if len(self.samples) > 0:
            data = [np.mean(item, axis=0) for item in self.samples]
            self.samples = []
            value = np.mean(np.square(data))
            decibels = 5.0*math.log10(value) + App.DB_OFFSET
            self.graph.add(decibels)

    def start(self):
        self.stop()     # make sure we're in a known state
        #self.timer = MultiTimer(interval=0.05, function=self.update, runonstart=False)
        #self.timer.start()
        #self.spectrogram.start()
        self.fft.start()
        self.graph.start()
        self.session.start()
        SYSLOG.info(f'Started {self.session}')

    def stop(self):
        if self.session:
            self.session.stop()
        #if self.timer:
        #   self.timer.stop()
        if self.fft:
            self.fft.stop()
        if self.graph:
            self.graph.stop()
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
