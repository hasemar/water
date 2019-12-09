Code Examples and Tutorials
============================

.. _pipe-example:

Pipe Class Examples
-------------------
The *Water.Pipe* class allows you to create a pipe object to apply flow calculations. It is useful to
start at a pump and create your pipe objects based on pipe size and/or material. You can add fittings
to each pipe object and calculate the major and minor losses through the pipe based on flow.


**Example #1:** Calculating the losses from a pump's discharge through a pipe network consisting of the following fittings:
    - 90 degree elbow, quantity 2
    - through-tee, quantity 1
    - branch-tee, quantity 1
    - gate valve, quantity 1

    The pipe is 4-inch schedule 40 steel pipe and 60 ft long.

.. code-block:: python  
   :linenos:

   from Water import Pipe
   
    # assign the flow you want to analyze in gallons per minute
    flow = 300       # gpm

    # create the pipe object
    pipe_1 = Pipe(length=60, size=4, kind='STEEL', sch=40)

    # add fittings to the pipe object 
    pipe_1.fitting(fitting_type='elbow_90', con_type='standard_threaded', qty=2)
    pipe_1.fitting('tee_through', 'standard_threaded', qty=1)
    pipe_1.fitting('tee_branch', 'standard_threaded', qty=1)
    pipe_1.fitting('valve', 'gate', qty=1) 

    # apply the get_losses function to compute head loss 
    losses = pipe_1.get_losses(flow)

    print('head loss at {} gpm = {:.2f} ft'.format(flow, losses))

>>> output: head loss at 300 gpm = 5.60 ft

You can get a list of fittings in the pipe object by using the *Pipe.fitting_info()* method.  

>>> print(pipe_1.fitting_info())  
       Fittings list: 
        elbow_90, standard_threaded: Kvalue = 0.899, qty = 2 
        tee_through, standard_threaded: Kvalue = 0.225, qty = 1 
        tee_branch, standard_threaded: Kvalue = 1.124, qty = 1 
        valve, gate: Kvalue = 0.275, qty = 1 

**Example #2:** Building from example #1, this is an example of finding the Total Dynamic Head for a pipe network consisting 
of a pump, pipe and fittings, and a tank at an elevated location.

.. Image:: pipe_ex2.png

.. code-block::  python  

    from Water import Pipe
   
    # assign the flow you want to analyze in gallons per minute
    flow = 300       # gpm
    L = 100          # ft

    # create the 2 pipe segments in the pipe network
    pipe_1 = Pipe(length=60, size=4, kind='STEEL', sch=40)
    pipe_2 = Pipe(length=20, size=2, kind='STEEL', sch=40)

    # add fittings to the pipe segments 
    pipe_1.fitting(fitting_type='elbow_90', con_type='standard_threaded', qty=2)
    pipe_1.fitting('tee_through', 'standard_threaded', qty=1)
    pipe_1.fitting('tee_branch', 'standard_threaded', qty=1)
    pipe_1.fitting('valve', 'gate', qty=1)

    pipe_2.fitting('elbow_90', 'standard_threaded', qty=2)

    # apply the get_losses function to compute major and minor losses 
    losses = pipe_1.get_losses(flow) + pipe_2.get_losses(flow)

    TDH = L + losses 

    print('Size Pump for {} gpm at {:.0f} feet of Head'.format(flow, TDH))

>>> output: Size Pump for 300 gpm at 153 feet of Head
-----------------------------------------



