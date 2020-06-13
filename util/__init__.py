from .log import SYSLOG
from .fft import Transforms
from .range import Range, Size
from .gradient import Gradient, Stop, Colour, Gradients 


class Theme(object):
    
    def __init__(self,data='red',spectrum='green',vu='yellow',background='black',text='white',gradient=None):
        self._data=data
        self._spectrum=spectrum
        self._vu=vu
        self._bg=background
        self._text=text
        self.gradients=Gradients()
        self.gradient=self.gradients()
    
    @property
    def data(self): return dict(fill=self._data)
    
    @property
    def spectrum(self): return dict(fill=self._spectrum)
    
    @property
    def vu(self): return dict(fill=self._vu)
    
    @property
    def background(self): return self._bg
    
    @property
    def axes(self): return dict(outline=self._text)
    
    def grid(self,solid=False):
        attrs = dict(fill = '#808080')
        if not solid:
            attrs['dash']=(2,5)
        return attrs 
        
    
    @property
    def labels(self): return dict(fill=self._text)
    
DefaultTheme=Theme()