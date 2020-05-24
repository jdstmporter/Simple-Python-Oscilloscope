'''
Created on 9 May 2020

@author: julianporter
'''
from util import Range, DefaultTheme
from ..graphic import Graphic

class SpectrumView(Graphic):

    def __init__(self, root, bounds=Range(-1,1), theme=DefaultTheme, xflen=513):
        super().__init__(root, bounds, theme)
        self.line = self.graph.create_line(-1, 0, -1, 0, **theme.spectrum)
        self.xflen = xflen
        self.points = [0]*2*self.xflen

    def fixSize(self,w,h):
        if w != self.width:
            self.width=w
            xscale = w / self.xflen
            for idx in range(self.xflen):
                self.points[2*idx] = idx*xscale
        self.height = h
        '''if s.height != self.height:
            self.height=s.height
            yscale = s.height / self.xflen
            for n in range(self.xflen): self.points[2*n+1]=self.height-n*yscale
        self.width=s.width'''


    def __call__(self,xformed):
        for index,value in enumerate(xformed):
            yVal = (1-self.range(value))*self.height
            self.points[2*index+1] = yVal
            ''''x=self.range(value)*self.width
            self.points[2*index]=x'''
        self.graph.coords(self.line, self.points)
