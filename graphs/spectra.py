'''
Created on 7 May 2020

@author: julianporter
'''
from numpy import fft, absolute, log2, zeros
import tkinter as tk
import tkinter.ttk as ttk
from .graphic import Graphic,Range

class Transforms(object):
    
    def __init__(self,size=1024):
        self.size=size
       
    @classmethod 
    def logNorm(cls,vector):
        return log2(absolute(vector))

    def powerSpectrum(self,data=[]):
        spec=fft.rfft(data,self.size)
        return Transforms.logNorm(spec)
        
    
    def rCepstrum(self,data=[]):
        reals = self.powerSpectrum(data)
        return fft.irfft(reals,self.size)
    
    def cxCepstrum(self,data=[]):
        spec = log2(fft.fft(data,self.size))
        return fft.ifft(spec,self.size)

    def powerRCepstrum(self,data=[]):
        return Transforms.logNorm(self.rCepstrum(data))

    def powerCxCepstrum(self,data=[]):
        return Transforms.logNorm(self.cxCepstrum(data))
    

    
class SpectrumView(Graphic):
    
    @classmethod
    def BaseWindow(cls,root):
        w=tk.Toplevel(root)
        content = ttk.Frame(w,width=300,height=500)
        content.grid(column=0,row=0,sticky=(tk.N,tk.S,tk.E,tk.W))
        w.columnconfigure(0, weight=1)
        w.rowconfigure(0, weight=1)
        return content
        
    
    def __init__(self,root,bounds=Range(-1,1),xscale=1,background='black',line='green',fftSize=1024):
        super().__init__(root,bounds,xscale,background,line)
        
        self.line = self.graph.create_line(-1,0,-1,0,fill=line)
        self.fft =Transforms(fftSize)
        self.buffer=[]
        
        self.xflen = 1+fftSize//2
        self.points= [0]*2*self.xflen
        
    def pack(self):
        s=self.size
        if s.width != self.width:
            self.width=s.width
            xscale = s.width / self.xflen
            for n in range(self.xflen): self.points[2*n]=n*xscale
        self.height=s.height
        
    def add(self,values):
        
        self.buffer.extend(values[::2])
        if len(self.buffer)>=self.fft.size:
            values = self.buffer[:self.fft.size]
            self.buffer=self.buffer[self.fft.size:]
            self.pack()
            
            xformed = self.fft.powerSpectrum(values)
            for index,value in enumerate(xformed):
                y=(1-self.range(value))*self.height
                self.points[2*index+1]=y
            self.graph.coords(self.line,self.points)
            
            
            
        
        
        
        
        
        
        
        
        
        
        
