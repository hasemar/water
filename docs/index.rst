Water Documentation
==================== 

This Python package was built to aid engineers in the design of common water system assets. 
It contains several python classes and helper functions that help analyze common scenarios such as pumping power, 
head loss, storage capacity, and PRV sizing.

Currently units are the U.S. water industry standard form:  

* Distance: feet (ft)    
* Head Loss: feet of water  (ft)  
* Time: seconds  (s)  
* Pressure:  pounds per square inch  (psi)  
* Flow: gallons per minute (gpm) 
* Velocity: feet per second  (fps)
* Volume: cubic feet (cuft), gallons (gal), acre feet (acft) *depending on the context*

Some helper functions, such as area and volume are not unit specific and as long as you maintain unit consistency
the units can be what ever you want. This reference will identify when a function will return specific units.

This project is currently in need of some serious opensource contributions! 
If you would like to contribute, visit my project `Github Page <https://github.com/hasemar/water>`.
  
Requirements
--------------

Most classes and functions just use the standard built-in libraries for Python 3.4+. However, the Pumps
class uses the following and are required in order to use it.

    - `Numpy <https://numpy.org/>`_

    - `Matplotlib <https://matplotlib.org/users/installing.html>`_


Contents
----------

.. toctree::

    code_reference
    tutorial
    data
    Github Page <https://github.com/hasemar/water>


Indices and tables
-------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Contribute!
-------------

Help make this package great! The `Water code repository <https://github.com/hasemar/water>`_ is on Github and I would love some help making it better. I have reached the top end of my programming knowledge (and time commitment). There are many things that would make this tool more useful. 
