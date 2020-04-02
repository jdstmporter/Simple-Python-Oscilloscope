Simple Python Oscilloscope
==========================

Introduction
------------

A lightweight python app that plots audioincoming at one of a device's microcphone channels.  Plotting is at audio bit-rates, so there is no squeezing of the useful spectrum down into the bottom 2% of the display.

The application is pure Python3 and should work on all major platforms (Linux, MacOS, Windows). In particular, it is sufficiently lightweight that it will run on small embedded Linux platforms, such as `Raspberry Pi`_ or BeagleBone_. 

Dependencies
~~~~~~~~~~~~

.. list-table::
     :header-rows: 1

     * - Package
       - Minimum version
     * - TCK/TK
       - 8.6
     * - Python
       - 3.7 [*]_
     * - numpy
       - 1.18
     * - python-sounddevice
       - 0.3.15 


.. [*] With the **tkinter** library as a part of
   the build 

Issues
------

- The code is not very robust; needs much better error checking / trapping
- Needs a proper logging system
- Do something with default input selection
- The main class is a wierd mix of application logic and GUI management; needs
  refactoring

TO-DO
-----

- It's only single-channel (averaging all channels together)
- Need spectrogram view
- Need to implement cursors, controls, etc, allow for zooms



.. _`Raspberry Pi`: http://www.raspberrypi.org
.. _BeagleBone: http://beagleboard.org
