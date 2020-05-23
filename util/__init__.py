from .log import SYSLOG
from .fft import Transforms
from .range import Range, Size
from .gradient import Gradient, Stop, Colour, GreyScaleGradient, RedGreenBlueGradient 

class Theme(object):
    
    def __init__(self,data='red',spectrum='green',vu='yellow',background='black',gradient=RedGreenBlueGradient):
        self._data=data
        self._spectrum=spectrum
        self._vu=vu
        self._bg=background
        self.gradient=gradient
    
    @property
    def data(self): return dict(fill=self._data)
    
    @property
    def spectrum(self): return dict(fill=self._spectrum)
    
    @property
    def vu(self): return dict(fill=self._vu)
    
    @property
    def background(self): return self._bg
    
DefaultTheme=Theme()