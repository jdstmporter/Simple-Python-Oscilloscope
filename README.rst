Simple Python Oscilloscope
==========================

Introduction
------------

A lightweight python app that plots audioincoming at one of a device's microcphone channels.  Plotting is at audio bit-rates, so there is no squeezing of the useful spectrum down into the bottom 2% of the display.

By intention the application is sufficiently lightweight that it will run on small embedded Linux platforms, such as `Raspberry Pi`_ or BeagleBone_.

Dependencies
~~~~~~~~~~~~

* **TCL/TK** >= 8.6
* **python** >= 3.7 [*]_
* **libasound2** >= 1.1.8

This application requires a pre-release version of the Python library **pyalsaaudio**, which may be obtained and
built as follows:

.. code:: bash

  git clone https://github.com/larsimmisch/pyalsaaudio.git
  cd pyalsaaudio.git
  git checkout jdstmporter-dev/card-detail
  python3 setup.py build
  python3 install --user   

The installation script (not yet available) will handl ethis aspect of installation. together with managing other dependencies.

.. [*] With the **tkinter** library as a part of
   the build

.. _`Raspberry Pi`: http://www.raspberrypi.org
.. _BeagleBone: http://beagleboard.org
