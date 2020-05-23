'''
Created on 21 May 2020

@author: julianporter
'''




import tkinter as tk

from util import Transforms, Range, DefaultTheme
from .spectra import Spectrogram, SpectrumView
from graphs.viewBase import RunnerBase, ViewBase


class SpectralView(ViewBase):
    class Runner(RunnerBase):
        def __init__(self, queue, callback, fft):
            super().__init__(queue,callback)
            self.fft=fft
            self.fftSize=fft.size
            
        def process(self):
            while len(self.buffer)>=self.fftSize:
                values = self.buffer[:self.fftSize]
                self.buffer=self.buffer[self.fftSize:]
                self.callback(self.fft.powerSpectrum(values))
            

    def __init__(self, root, bounds=Range(-1,1), theme=DefaultTheme, fftSize=1024, average=10):
        super().__init__(root,bounds)
        self.average = average
        self.fftSize = fftSize
        self.fft = Transforms(self.fftSize)
        self.spectrogram = Spectrogram(self.root, self.range,
                                       theme, self.fft.xflen)
        self.spectrum = SpectrumView(self.root, self.range,
                                     theme, self.fft.xflen)
        self.viewers = [self.spectrum, self.spectrogram]


    def setSampleRate(self, rate=48000):
        self.fft = Transforms(self.fftSize, rate)
        
    def makeThread(self):
        def callback(data):
            for viewer in self.viewers:
                viewer(data)
        return SpectralView.Runner(self.queue, callback, self.fft)

    def start(self):
        self.spectrogram.start()
        super().start()

    def stop(self):
        super().stop()
        self.spectrogram.stop()

    def configure(self, **kwargs):
        if 'height' in kwargs: kwargs['height'] = kwargs['height']//2
        self.spectrogram.configure(**kwargs)
        self.spectrum.configure(**kwargs)

    def pack(self):
        self.spectrogram.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.spectrogram.graph.config(scrollregion=self.spectrogram.graph.bbox(tk.ALL))
        self.spectrum.grid(column=0, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        
'''
class SpectralView(object):
    class Runner(threading.Thread):
        def __init__(self, qu, callback, fft):
            super().__init__()
            self.buffer=[]
            self.queue=qu
            self.callback=callback
            self.fft=fft
            self.fftSize=fft.size
            self.active=False

        def run(self):
            self.active=True
            while self.active:
                item=self.queue.get(block=True)
                self.buffer.extend(item)
                while len(self.buffer)>=self.fftSize:
                    values = self.buffer[:self.fftSize]
                    self.buffer=self.buffer[self.fftSize:]
                    self.callback(self.fft.powerSpectrum(values))

        def shutdown(self):
            self.active=False

    def __init__(self, root, bounds=Range(-1,1), background='black', line='red', 
                 gradient=Gradient(), fftSize=1024, average=10):
        self.root = root
        self.range = bounds
        self.queue = queue.Queue()
        self.thread = None
        self.average = average
        self.fftSize = fftSize
        self.fft = Transforms(self.fftSize)
        self.spectrogram = Spectrogram(self.root, self.range,
                                       background, line, gradient, self.fft.xflen)
        self.spectrum = SpectrumView(self.root, self.range,
                                     background, line, self.fft.xflen)
        self.viewers = [self.spectrum, self.spectrogram]


    def setSampleRate(self, rate=48000):
        self.fft = Transforms(self.fftSize, rate)

    def start(self):
        self.spectrogram.start()
        def callback(data):
            for viewer in self.viewers:
                viewer(data)
        self.thread = SpectralView.Runner(self.queue, callback, self.fft)
        self.thread.start()

    def stop(self):
        if self.thread:
            self.thread.shutdown()
            self.thread = None
        self.spectrogram.stop()

    def add(self, values):
        self.queue.put(values, block=False)

    def configure(self, width=0, height=0):
        self.spectrogram.configure(width=width, height=height//2)
        self.spectrum.configure(width=width, height=height//2)

    def pack(self):
        self.spectrogram.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.spectrogram.graph.config(scrollregion=self.spectrogram.graph.bbox(tk.ALL))
        self.spectrum.grid(column=0, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))
'''
