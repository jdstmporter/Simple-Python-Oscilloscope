'''
Created on 21 May 2020

@author: julianporter
'''




from util import Transforms, Range, DefaultTheme, SYSLOG
from graphs.viewBase import RunnerBase, ViewBase
import numpy as np

class Windower(object):
    
    def __init__(self,wndw=[0.8,1,0.8],xflen=513):
        self.length=len(wndw)
        self.xflen=xflen
        self.ffts=np.zeros((self.length,self.xflen))
        self.windower=np.array(wndw)
        self.offset=self.length//2
        self.pos=0
    
    def apply(self,ffts,offset=0):
        #wndw=np.roll(self.windower,offset+1)
        return np.average(ffts,axis=0) #,weights=wndw)
        
    def __call__(self,data):
        self.pos=(1+self.pos)%self.length
        self.ffts[self.pos]=data
        #wndw=np.roll(self.windower,1+self.pos)
        return np.average(self.ffts,axis=0) #,weights=wndw)



class SpectralView(ViewBase):
    
    NORM = 0
    PHASE = 1
    CEPSTRUM = 8
    
    class Runner(RunnerBase):
        def __init__(self, queue, callback, fft, overlap):
            super().__init__(queue,callback)
            self.fft=fft
            self.fftSize=fft.size
            self.windower=Windower(xflen=fft.xflen)
            self.overlap=int(overlap*self.fftSize)
            self.mode = SpectralView.NORM
            
            self.actions = {
                SpectralView.NORM:  self.fft.powerSpectrum,
                SpectralView.PHASE: self.fft.spectralPhase,
                SpectralView.CEPSTRUM: self.fft.cepstrum 
            }
            self.action = self.actions[self.mode]
        
        
            
        
            
            
        def process(self):
            while len(self.buffer)>=self.fftSize:
                values = self.buffer[:self.fftSize]
                self.buffer=self.buffer[self.fftSize:]
                latest=self.action(values)
                self.callback(self.windower(latest))
        
        def setMode(self,mode):
            self.mode=mode
            self.action=self.actions[mode]
            SYSLOG.info(f'mode is {mode}')

    def __init__(self, root, bounds=Range(-1,1), theme=DefaultTheme, fftSize=1024,overlap=0.9):
        super().__init__(root,bounds)
        self.theme=theme
        self.fftSize = fftSize
        self.fft = Transforms(self.fftSize)
        self.overlap=overlap
        #self.spectrogram = Spectrogram(self.root, self.range,
        #                               theme, self.fft.xflen)
        #self.spectrum = SpectrumView(self.root, self.range,
        #                             theme, self.fft.xflen)
        
    def addViewer(self,klass,**kwargs):
        viewer=klass(self.root,self.range,self.theme,self.fft.xflen,**kwargs)
        self.viewers.append(viewer)
        return viewer

        
    def makeThread(self):
        def callback(data):
            for viewer in self.viewers:
                viewer(data)
        return SpectralView.Runner(self.queue, callback, self.fft, self.overlap)

    def start(self):
        for view in self.viewers:
            view.start()
        super().start()

    def stop(self):
        super().stop()
        for view in self.viewers:
            view.stop()

    def configure(self, **kwargs):
        if 'mode' in kwargs:
            self.thread.setMode(kwargs['mode'])
            del kwargs['mode']
        #if 'height' in kwargs: kwargs['height'] = kwargs['height']//2
        for v in self.viewers: 
            v.configure(**kwargs)

    def pack(self):
        #self.spectrogram.grid(column=0, row=0, sticky=Stick.ALL)
        #self.spectrogram.scroll.grid(column=0,row=1, sticky=Stick.ALL)
        #self.spectrogram.graph.config(scrollregion=self.spectrogram.graph.bbox(tk.ALL))
        #self.spectrum.grid(column=0, row=2, sticky=Stick.ALL)
        pass
    
    
          
        
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
