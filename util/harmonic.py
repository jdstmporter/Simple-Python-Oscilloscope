'''
Created on 21 Jul 2020

@author: julianporter
'''


import numpy as np

class HarmonicTransform(object):
    '''
    From https://gist.github.com/fasiha/957035272009eb1c9eb370936a6af2eb
    '''
    
    def __init__(self,size=1024,nProducts=10,sampleRate=48000):
        self.fftSize=size
        self.nProducts=nProducts
        frequencies = np.arange(self.fftSize) / self.fftSize
        positive = frequencies[frequencies < 0.5]
        self.nPositive = positive.size
        self.smallestLength = int(np.ceil(self.nPositive / nProducts))
        self._freqs = positive[:self.smallestLength] * sampleRate
       
    @property
    def freqs(self):
        return self._freqs 
        
    def harmonicProduct(self,data=[]):
        xformed = np.fft.fft(data, self.fftSize)[:self.nPositive]
        products = xformed[:self.smallestLength].copy()
        for i in range(2, self.nProducts + 1):
            products *= xformed[::i][:self.smallestLength]
        return products
        

def hps(data, nProducts, fftSize=1024, sampleRate=1):
    """Harmonic product spectrum of a vector.

    This algorithm can be used for fundamental frequency detection. It evaluates
    the magnitude of the FFT (fast Fourier transform) of the input signal, keeping
    only the positive frequencies. It then element-wise-multiplies this spectrum
    by the same spectrum downsampled by 2, then 3, ..., finally ending after
    numProd downsample-multiply steps.

    Here, "downsampling a vector by N" means keeping only every N samples:
    downsample(v, N) = v[::N].

    Of course, at each step, a vector of data is multiplied by a vector *smaller*
    than it: the algorithm specifies that the extra elements at the end of the
    onger vector be ignored. This implies that the output will be ceil(len(x) /
    numProd) long, so at each step, we only consider this many elements.

    References
    ----------
    See Gareth Middleton, Pitch Detection Algorithms (2003) at
    http://cnx.org/contents/i5AAkZCP@2/Pitch-Detection-Algorithms#idp2614240
    (accessed September 2016).

    Parameters
    ----------
    data : array_like
        Time-samples of data
    nProducts : int
        Number of products to evaluate the harmonic product spectrum over.
    fftSize : int, defaults to 1024
        The length of the FFT. Almost always this is greater than the length of data,
        with data being zero-padded before the FFT. This is helpful for two reasons:
        more zero-padding means more interpolation in the spectrum (a smoother
        spectrum). Also, FFT lengths with low prime factors (i.e., products of 2,
        3, 5, 7) are usually (much) faster than those with high prime factors. The
        default is fftSize = len(data). By way of example, if len(data) = 4001, this
        default might take much more time to run than fftSize = 4096, since 4001 is
        prime while 4096 is a power of 2.
    sampleRate : float, defaults to 1
        The sample rate of data, in samples per second (Hz). Used only to format the
        returned vector of frequencies.

    Returns
    -------
    products : array
        Spectrum vector with ceil(fftSize / (2 * nProducts)) elements.
    frequencies : array
        Vector of frequencies corresponding to the spectrum in products. Runs from 0 to
        roughly (sampleRate / (2 * nProducts)) Hz.
    """
    
    # Evaluate FFT. f is the frequencies corresponding to the spectrum xf
    frequencies = np.arange(fftSize) / fftSize
    xformed = np.fft.fft(data, fftSize)
    # Keep magnitude of spectrum at positive frequencies
    xformed = np.abs(xformed[frequencies < 0.5])
    frequencies = frequencies[frequencies < 0.5]
    nFreqs = frequencies.size
    
    # Downsample-multiply
    smallestLength = int(np.ceil(nFreqs / nProducts))
    products = xformed[:smallestLength].copy()
    for i in range(2, nProducts + 1):
        products *= xformed[::i][:smallestLength]
    frequencies = frequencies[:smallestLength] * sampleRate
    return (products, frequencies)



