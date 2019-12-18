Water Documentation
==================== 

This Python package was built to aid engineers in the design of common water system assets. 
It contains several python classes and helper functions that help analyze common scenarios such as pumping power, 
head loss, storage capacity, and PRV sizing.

Currently units are in industry standard form:  

* Distance: feet (ft)    
* Head Loss: feet of water  (ft)  
* Time: seconds  (s)  
* Pressure:  pounds per square inch  (psi)  
* Flow: gallons per minute (gpm) 
* Velocity: feet per second  (fps)
* Volume: cubic feet (cuft), gallons (gal), acre feet (acft) *depending on the context*

Some helper functions, such as area and volume are not unit specific and as long as you maintain unit consistency
the units can be what ever you want. This reference will identify when a function will return specific units.
  

.. toctree::

    code_reference
    tutorial
    data


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
