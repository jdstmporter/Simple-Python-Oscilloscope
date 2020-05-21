'''
Created on 9 May 2020

@author: julianporter
'''

from ..graphic import Graphic
from util import Range

class SpectrumView(Graphic):
        
    def __init__(self,root,bounds=Range(-1,1),xscale=1,background='black',line='green',xflen=513):
        super().__init__(root,bounds,xscale,background,line)
        self.line = self.graph.create_line(-1,0,-1,0,fill=line)
        self.xflen=xflen
        self.points= [0]*2*self.xflen
        
    def fixSize(self):
        s=self.size
        #if s.width != self.width:
        #    self.width=s.width
            #xscale = s.width / self.xflen
            #for n in range(self.xflen): self.points[2*n]=n*xscale
        #self.height=s.height
        if s.height != self.height:
            self.height=s.height
            yscale = s.height / self.xflen
            for n in range(self.xflen): self.points[2*n+1]=self.height-n*yscale
        self.width=s.width
        
          
    def __call__(self,xformed):
        self.fixSize()
        for index,value in enumerate(xformed):
            #y=(1-self.range(value))*self.height
            #self.points[2*index+1]=y
            x=self.range(value)*self.width
            self.points[2*index]=x
        self.graph.coords(self.line,self.points)
            
            