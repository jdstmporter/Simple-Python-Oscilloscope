'''
Created on 7 Mar 2020

@author: julianporter
'''

from itertools import chain
from .graphic import Graphic,Range


      
        
        
class Graph(Graphic):
    
    def __init__(self,root,bounds=Range(-1,1),xscale=1,background='black',line='red'):
        super().__init__(root,bounds,xscale,background,line)
        
        self.basePoints=[-1,self.height,-1,self.height]
        self.line = self.graph.create_line(*self.basePoints,fill=line)
        
        
        
        
    def bind(self,binding,callback):
        self.graph.bind(binding,callback)
        
    def grid(self,**kwargs):
        self.graph.grid(**kwargs)
  
    def pack(self):
        s=self.size
        if s.width!=self.width:
            self.width=s.width
            self.xs=list(range(0,self.width))
        self.height=s.height
    
    def __len__(self):
        return len(self.points)
        
    def add(self,y):
        self.pack()
        
        #x=self.xscale*self.N/2
        y=(1.0-self.range(y))*self.height
        self.ys=(self.ys+[y])[-self.width:]
        points=list(chain(*zip(self.xs,self.ys)))
        #print(f'{y}')
        #self.points+=[x,y]
        #if self.N>2*self.width:
        #    self.points=self.points[2:]
        #    for i in range(0,self.N,2): self.points[i]-=self.xscale
        if len(self.ys)>=2:
            self.graph.coords(self.line,points)
        
        
        
    def clear(self):
        #self.points=[0,self.height,0,self.height]
        self.ys=[]
        self.graph.coords(self.line,self.basePoints)
        
    
          
        