#!/usr/bin/env python3

'''
Created on 3 Mar 2020

@author: julianporter
'''

import tkinter as tk
import tkinter.ttk as ttk
from portaudio import PCMSystem, PCMSession, PCMSessionDelegate
from graphs import Graph, Range, SpectrumView, Spectrogram,Gradient, Stop,Colour,SpectralBase
from multitimer import MultiTimer
from collections import OrderedDict
import math
import statistics
import numpy as np


def safe(action):
    try:
        action()
    except:
        pass
    
    
    

class App(PCMSessionDelegate):
    
    BUFFER_LENGTH=64
    DB_OFFSET=-10.0*math.log10(32768.0)
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.protocol('WM_DELETE_WINDOW',self.shutdown)
        
        
        self.content = ttk.Frame(self.root,width=300,height=500)
        self.content.grid(column=0,row=0,sticky=(tk.N,tk.S,tk.E,tk.W))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        pcm = PCMSystem()
        self.devices = OrderedDict()
        for dev in pcm.inputs() : 
            self.devices[dev.name]=dev
            print(f'Device : {dev.name} {dev.maxIn} {dev.rate}')
        
        self.currentDevice = tk.StringVar()
        self.currentDevice.set(self[0].name)
        
        self.cards=ttk.Combobox(self.content,textvariable = self.currentDevice,
                                values = self.names, justify = tk.LEFT)
        self.cards.bind('<<ComboboxSelected>>',self.changeCard)
        self.cards.grid(column=0,row=0,columnspan=4,sticky=(tk.N,tk.S,tk.E,tk.W))
        
        
        self.graph=Graph(self.content, bounds=Range(-40,10))
        self.graph.grid(column=0,row=1,columnspan=4,sticky=(tk.N,tk.S,tk.E,tk.W))
        self.graph.bind('<Button-1>',self.onClick)
        
        self.spec = tk.Toplevel(self.root,width=800,height=300)
        self.spectrum=SpectrumView(self.spec,bounds=Range(-40,40),xflen=513)
        self.spectrum.configure(width=800,height=300)
        self.spectrum.pack()
        
        self.spectro = tk.Toplevel(self.root,width=800,height=300)
        self.spectrogram=Spectrogram(self.spectro,bounds=Range(-40,40),
                                     gradient=Gradient(Stop(Colour.Green,offset=0), 
                                                       Stop(Colour.Yellow,offset=0.5),
                                                       Stop(Colour.Orange,offset=1.0)),xflen=513)
        self.spectrogram.configure(width=800,height=300)
        self.spectrogram.pack()
        
        self.fft = SpectralBase(fftSize=1024,viewers=[self.spectrum,self.spectrogram])
        
        self.startButton = ttk.Button(self.content,text='Start',command=self.start)
        self.stopButton = ttk.Button(self.content,text='Stop',command=self.stop)
        self.clearButton = ttk.Button(self.content,text='Clear',command=self.graph.clear)
        
        self.clearButton.grid(column=0,row=2,sticky=(tk.N,tk.S,tk.W))
        self.startButton.grid(column=2,row=2,sticky=(tk.N,tk.S,tk.E))
        self.stopButton.grid(column=3,row=2,sticky=(tk.N,tk.S,tk.E,tk.W))
        
        for column in [0,2,3] : self.content.columnconfigure(column, weight=1)
        self.content.rowconfigure(1, weight=1)
        
        
        self.mean=[]
        

        self.timer=None 
        self.samples=[]
        self.raw=[]
        self.session=PCMSession(self[0],delegate=self)
        
    def onClick(self,event):
        print(f'Click on {event.widget}')
        canvas = event.widget
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)
        print(f'{self.graph.size} : ({event.x},{event.y}) -> ({x},{y})')
        
    @property
    def names(self):
        return list(self.devices.keys())
        
    def __getitem__(self,index):
        if type(index)==str:
            return self.devices[index]
        else:
            return self.devices[self.names[index]]
            
          

        
    def changeCard(self,event=None):
        try:
            if self.session is None:
                return
            
            dev=self[self.currentDevice.get()]
            
            if dev==self.session.pcm:
                return
            else:
                print(f'Changing to {dev}')
                self.stop()
                self.session=PCMSession(dev)
                self.spec.setSampleRate(self.session.samplerate)
                self.start()
                
        except:
            print(f'{event}')          
    
    def __call__(self,n,time,data=[],raw=[]):
        self.samples.extend(data)
        if len(raw)>0:
            self.raw.extend(np.mean(raw,axis=1))
        #d=datetime.now()
        #print(f'{d.hour}:{d.minute}:{d.second}:{d.microsecond} : {len(data)}')
            
        
        
        
    def update(self):
        if len(self.samples)>0:
            data=self.samples[:]
            self.samples=[]
            value=statistics.pvariance(data,mu=0)
            db=5.0*math.log10(value)+App.DB_OFFSET
            self.graph.add(db)
            raw=self.raw[:]
            self.raw=[]
            self.fft.add(raw)
        
            
            
  


        
        
        
    def start(self):
        self.stop()     # make sure we're in a known state
        self.timer=MultiTimer(interval=0.05,function=self.update,runonstart=False)
        self.timer.start()
        self.session.start()
        print(f'Started {self.session}')
        

    def stop(self):
        if self.session: self.session.stop()
        if self.timer: self.timer.stop()
        self.timer=None

        
    def shutdown(self):
        self.stop()
        self.root.destroy()
        
    def run(self):
        try:
            self.start()
            self.root.mainloop()
        except:
            pass
        finally:
            self.stop()
    
    
    


       
        
          


if __name__ == '__main__':
    
    app=App()
    app.run()
    
   
    
    