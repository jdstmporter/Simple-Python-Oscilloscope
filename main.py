#!/usr/bin/env python3

'''
Created on 3 Mar 2020

@author: julianporter
'''

import tkinter as tk
import tkinter.ttk as ttk
from portaudio import PCMSystem, PCMSession, PCMSessionDelegate, Direction
from graphs import Graph, Range
from multitimer import MultiTimer
from collections import OrderedDict
import math
import statistics

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
        self.content.grid(column=0,row=0)
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        pcm = PCMSystem()
        self.devices = OrderedDict()
        for dev in pcm.inputs() : self.devices[str(dev)]=dev
        
        self.currentDevice = tk.StringVar()
        self.currentDevice.set(self[0])
        
        self.cards=ttk.Combobox(self.content,textvariable = self.currentDevice,
                                values = self.names, justify = tk.LEFT)
        self.cards.bind('<<ComboboxSelected>>',self.changeCard)
        self.cards.grid(column=0,row=0,columnspan=4,sticky=(tk.N,tk.S,tk.E,tk.W))
        
        
        self.graph=Graph(self.content, bounds=Range(-40,10))
        self.graph.grid(column=0,row=1,columnspan=4,sticky=(tk.N,tk.S,tk.E,tk.W))
        self.graph.bind('<Button-1>',self.onClick)
        
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
        self.session=PCMSession(self[0],delegate=self)
        
    def onClick(self,event):
        print(f'Click on {event.widget}')
        canvas = event.widget
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)
        print(f'{self.graph.size()} : ({event.x},{event.y}) -> ({x},{y})')
        
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
                self.start()
                
        except:
            print(f'{event}')          
    
    def __call__(self,n,time,data=[]):
        self.samples.extend(data)
        
        
    def update(self):
        if len(self.samples)>0:
            data=self.samples[:]
            self.samples=[]
            value=statistics.pvariance(data,mu=0)
            db=5.0*math.log10(value)+App.DB_OFFSET
            self.graph.add(db)
  


        
        
        
    def start(self):
        self.stop()     # make sure we're in a known state
        self.timer=MultiTimer(interval=0.1,function=self.update,runonstart=False)
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
    
   
    
    